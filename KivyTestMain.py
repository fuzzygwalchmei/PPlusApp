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
import requests
import json

current_organisation ="default value"

class StudentListButton(ListItemButton):
    pass

#Code for Login_Screen
class Kivy_Test_Login(Screen):
    userName_Input = ObjectProperty()
    passWord_Input = ObjectProperty()


    def doLogin(self):
        doUserName = self.userName_Input.text
        doPassWord = self.passWord_Input.text
        parameters = {"email": doUserName, "password": doPassWord}
        global myUserID
        global AuthToken


        response = requests.post("http://staging.purchaseplus.com/access/api/auth/sign_in",parameters)
        dataset = response.json()
        print(dataset.keys())

        response_status=response.status_code
        AuthToken = {"access_token": response.headers["access-token"], "uid":response.headers["uid"], "client": response.headers["client"]}
        response_content = dataset["data"]
        myAttributes = response_content["attributes"]


        if response.status_code == 200:
            self.ids.BottomLabel.text = str(response_status)
            self.parent.current = "Main_Screen"
            myUserID = response_content["id"]
            current_organisation = myAttributes["default_organisation"]["name"]


        else:
            self.ids.BottomLabel.text = "Your username or password was incorrect. Status: " + str(response_status)

#Code for Main_Screen
class Kivy_Test_Main(Screen):
    current_organisation = StringProperty("default")
    myOrgList = ObjectProperty()
    global orgList
    orgList = {}

    def showUserDetails(self):
        response = requests.get("http://staging.purchaseplus.com/access/api/users/"+myUserID, headers=AuthToken)
        responseJSON = response.json()
        userDetails = responseJSON["data"]
        print(userDetails.keys())
        for each in userDetails.keys():
            print(userDetails[each])
        self.Main_Body.text = userDetails



    def getOrgList(self):
        response = requests.get("http://staging.purchaseplus.com/access/api/users/"+myUserID+"/organisations", headers=AuthToken)
        responseJSON = response.json()
        orgDataset = responseJSON["data"]
        for each in orgDataset:
            newkey = each["attributes"]["name"]
            newdata = each["id"]
            orgList[newkey] = newdata
            self.myOrgList.adapter.data.extend([newkey])
        self.myOrgList._trigger_reset_populate()

    pass


#Build Main App
class KivyTestApp(App):
    def build(self):
        #setup screen_manager and add screens
        screen_manager = ScreenManager()
        screen_manager.add_widget(Kivy_Test_Login(name="Login_Screen"))
        screen_manager.add_widget(Kivy_Test_Main(name="Main_Screen"))
        screen_manager.current = "Login_Screen"

        return screen_manager


if __name__ == '__main__':
    KivyTestApp().run()
