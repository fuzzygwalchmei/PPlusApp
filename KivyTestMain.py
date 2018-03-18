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


#Code for Login_Screen
class Kivy_Test_Login(Screen):
    userName_Input = ObjectProperty()
    passWord_Input = ObjectProperty()
    response_status = StringProperty()
    def doLogin(self):
        doUserName = self.userName_Input.text
        doPassWord = self.passWord_Input.text
        parameters = {"email": doUserName, "password": doPassWord}

        response = requests.post("http://staging.purchaseplus.com/access/api/auth/sign_in",parameters)
        response_status=response.status_code
        response_header = json.loads(response.headers.decode('utf-8'))
        response_content = json.loads(response.content.decode('utf-8'))

        if response.status_code == 200:
            self.ids.BottomLabel.text = str(response_status)
            self.parent.current = "Main_Screen"
            print(response_header)
            print(response_content)
        else:
            self.ids.BottomLabel.text = "Your username or password was incorrect. Status: " + str(response_status)

#Code for Main_Screen
class Kivy_Test_Main(Screen):
    pass


'''
class screen_manager(ScreenManager):
    pass

#setup screen_manager and add screens
screen_manager = ScreenManager()
screen_manager.add_widget(Kivy_Test_Login(name="Login_Screen"))
screen_manager.add_widget(Kivy_Test_Main(name="Main_Screen"))
screen_manager.current = "Login_Screen"
'''

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
