from kivy.app import App
from kivy.properties import ObjectProperty,StringProperty

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton



class InputFieldArea(BoxLayout):
    
    value = StringProperty("WoW")
    buttonMid_id = ObjectProperty()

    def add_one(self):
        #Increase the value by 0.1
        myString = self.buttonMid_id.text
        if myString == "None":
            value = 0
        elif myString == "":
            value = 0
        else:
            value = float(myString)
        value = round(value + 0.1, 2)
        self.buttonMid_id.text = str(value)

    def substract_one(self):
        #Decrease the value by 0.1
        myString = self.buttonMid_id.text
        if myString == "None":
            value = 0
        elif myString == "":
            value = 0
        else:
            value = float(myString)

        value = round(value - 0.1, 2)
        if value <0:
            value = 0
        self.buttonMid_id.text = str(value)

class CenteredTextArea(RelativeLayout):
    pass
    

class ApplicationMainFrame(BoxLayout):
    pass


class TestApp(App):

    def build(self):
        self.title="Main Windows"
        return ApplicationMainFrame() 

     

if __name__ == '__main__':
    TestApp().run()
