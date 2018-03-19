# PPLusApp.py

from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.lang import Builder

Builder.load_file('PPlusLoginScreen.kv')
Builder.load_file('PPlusMainScreen.kv')
#Builder.load_file('box3.kv')

class Ex10(GridLayout):
    pass

class PPlusApp(App):
    def build(self):
        self.x=150
        self.y=400
        return Ex10()

if __name__=='__main__':
    PPlusApp().run()
