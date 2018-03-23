from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.listview import ListItemButton
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
import requests
import json


class StudentListButton(ListItemButton):
    pass


#Code for Login_Screen
class PPlusLoginScreen(Screen):
    userName_Input = ObjectProperty()
    passWord_Input = ObjectProperty()

    def doLogin(self):
        doUserName = self.userName_Input.text
        doPassWord = self.passWord_Input.text

        parameters = {"email": doUserName, "password": doPassWord}
        global myUserID
        global AuthToken
        global myAttributes
        global Gcurrent_organisation


        #MB API Login
        response = requests.post("http://staging.purchaseplus.com/access/api/auth/sign_in",parameters)
        dataset = response.json()
        response_status=response.status_code

        #Check for response
        if response.status_code == 200:
            self.parent.current = "Main_Screen"
            response_content = dataset["data"]
            myAttributes = response_content["attributes"]
            myUserID = response_content["id"]
            Gcurrent_organisation = myAttributes["default_organisation"]["name"]
            self.parent.get_screen("Main_Screen").ids.UserButton.text=response.headers["uid"]
            self.parent.get_screen("Main_Screen").ids.OrgButton.text=Gcurrent_organisation
            AuthToken = {"access_token": response.headers["access-token"], "uid":response.headers["uid"], "client": response.headers["client"]}
            print(Gcurrent_organisation)
        #post status error if failed
        else:
            self.ids.BottomLabel.text = "Your username or password was incorrect. Status: " + str(response_status)

#Code for Main_Screen
class PPlusMainScreen(Screen):
    #current_organisation = StringProperty("default")
    myOrgList = ObjectProperty()
    global orgList
    orgList = {}
    myOrgList=("replace me")

    def getDataList(self, url):
        baseURL = "http://staging.purchaseplus.com"
        response = requests.get(baseURL+url, headers=AuthToken)
        responseJSON = response.json()
        with open('result.json', 'w') as fp:
            json.dump(responseJSON, fp)
        returnData = responseJSON["data"]
        return returnData


    #Display User information
    def showUserDetails(self):
        functionURL="/access/api/users/"+myUserID
        userDetails = self.getDataList(functionURL)
        self.ids.MainBody.text = "My UID: "+str(myUserID)+"\n"+"My Email: "+myAttributes["email"]


    #Display a list of Orgs
    def getOrgList(self):
        OrgList = {}
        myTempOrgList =[]
        functionURL="/access/api/users/"+myUserID+"/organisations"
        orgDataset = self.getDataList(functionURL)
        for orgItem in orgDataset:
            newkey = orgItem["id"]
            newdata = orgItem["attributes"]["name"]
            orgList[newkey] = newdata
            myTempOrgList.append(newdata)
            #self.myOrgList.adapter.data.extend([newkey])
        #self.myOrgList._trigger_reset_populate()
        myOrgList = tuple(myTempOrgList)
        self.ids.OrgButton.values = myOrgList
        self.ids.MainBody.text = "clicked"




    def orgClicked(self):
        global Gcurrent_organisation
        dataset = ""

        if orgList:
            #orgIDTemp = orgList.keys(orgList[self.ids.OrgButton.text])
            functionURL = "/access/api/organisations/"+orgIDTemp
            print(functionURL)
            orgDetails = self.getDataList(functionURL)
            print(Gcurrent_organisation)
            Gcurrent_organisation = orgList[self.ids.OrgButton.text]
            print(orgList[Gcurrent_organisation])
            '''
            for each in orgDetails:
                dataset = each + orgList[each]+"\n"
                print(each)
            newText = dataset
            self.ids.MainBody.text = newText
            '''



#Build Main App
class PPlusApp(App):
    def build(self):
        #setup screen_manager and add screens
        screen_manager = ScreenManager()
        screen_manager.add_widget(PPlusLoginScreen(name="Login_Screen"))
        screen_manager.add_widget(PPlusMainScreen(name="Main_Screen"))
        screen_manager.current = "Login_Screen"

        return screen_manager


if __name__ == '__main__':
    PPlusApp().run()
