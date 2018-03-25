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

class MyGlobals(object):
    """docstring for MyGlobals."""
    def __init__(self):
        super(MyGlobals, self).__init__()
        self.myUserID = [] #[id, name, email]
        self.current_organisation = [] #[id, name]
        self.AuthToken = {} #{client, uid, access_token}
        self.orgList = {} #{ID: {id, name}}
        self.myAttributes = {} #{id, default org{}, type, email}

    def getOrgKey(self, search_value):
        for key in PPlusGlobals.orgList:
            if PPlusGlobals.orgList[key]["name"] == search_value:
                return key



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


        #MB API Login
        response = requests.post("http://staging.purchaseplus.com/access/api/auth/sign_in",parameters)
        dataset = response.json()
        response_status=response.status_code

        #Check for response
        if response.status_code == 200:
            self.parent.current = "Main_Screen"
            response_content = dataset["data"]
            PPlusGlobals.myAttributes = response_content["attributes"]
            PPlusGlobals.myUserID = response_content["id"]
            PPlusGlobals.current_organisation = [PPlusGlobals.myAttributes["default_organisation"]["id"],PPlusGlobals.myAttributes["default_organisation"]["name"]]
            self.parent.get_screen("Main_Screen").ids.UserButton.text=response.headers["uid"]
            self.parent.get_screen("Main_Screen").ids.OrgButton.text=PPlusGlobals.current_organisation[1]
            PPlusGlobals.AuthToken = {"access_token": response.headers["access-token"], "uid":response.headers["uid"], "client": response.headers["client"]}
            print(PPlusGlobals.current_organisation)
        #post status error if failed
        else:
            self.ids.BottomLabel.text = "Your username or password was incorrect. Status: " + str(response_status)

#Code for Main_Screen
class PPlusMainScreen(Screen):
    #current_organisation = StringProperty("default")
    myOrgList = ObjectProperty()

    def getDataList(self, url):
        baseURL = "http://staging.purchaseplus.com"
        response = requests.get(baseURL+url, headers=PPlusGlobals.AuthToken)
        responseJSON = response.json()
        with open('result.json', 'w') as fp:
            json.dump(responseJSON, fp)
        returnData = responseJSON["data"]
        return returnData


    #Display User information
    def showUserDetails(self):
        functionURL="/access/api/users/"+PPlusGlobals.myUserID
        userDetails = self.getDataList(functionURL)
        self.ids.MainBody.text = "My UID: "+str(PPlusGlobals.myUserID)+"\n"+"My Email: "+PPlusGlobals.myAttributes["email"]


    #Display a list of Orgs
    def getOrgList(self):
        myTempOrgList =[]
        functionURL="/access/api/users/"+PPlusGlobals.myUserID+"/organisations"
        orgDataset = self.getDataList(functionURL)
        for orgItem in orgDataset:
            newkey = orgItem["id"]
            newdata = orgItem["attributes"]["name"]
            PPlusGlobals.orgList[newkey] = {"id": newkey, "name": newdata}
            myTempOrgList.append(newdata)
            #self.myOrgList.adapter.data.extend([newkey])
        #self.myOrgList._trigger_reset_populate()
        myOrgList = tuple(myTempOrgList)
        self.ids.OrgButton.values = myOrgList
        self.ids.MainBody.text = PPlusGlobals.current_organisation[1]


    def orgClicked(self):
        dataset = ""
        if PPlusGlobals.orgList:
            orgIDTemp = PPlusGlobals.current_organisation[0]
            functionURL = "/access/api/organisations/"+str(orgIDTemp)
            orgDetails = self.getDataList(functionURL)
            print("current Org: ", PPlusGlobals.current_organisation)
            search_value = self.ids.OrgButton.text
            print("Search Value: ", search_value)
            NewOrgID = PPlusGlobals.getOrgKey(search_value)
            PPlusGlobals.current_organisation[0] = NewOrgID
            PPlusGlobals.current_organisation[1] = PPlusGlobals.orgList[NewOrgID]["name"]
            print("new current org: ", PPlusGlobals.current_organisation[0]," ", PPlusGlobals.current_organisation[1])



#Build Main App
class PPlusApp(App):
    def build(self):
        #setup screen_manager and add screens
        screen_manager = ScreenManager()
        screen_manager.add_widget(PPlusLoginScreen(name="Login_Screen"))
        screen_manager.add_widget(PPlusMainScreen(name="Main_Screen"))
        screen_manager.current = "Login_Screen"


        return screen_manager

PPlusGlobals = MyGlobals()
if __name__ == '__main__':
    PPlusApp().run()
