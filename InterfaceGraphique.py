from kivy.app import App
from kivy.config import Config 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox


class CottrellCurveBox(BoxLayout):
    pass

class ICurveBox(BoxLayout):
    pass

class CoxCurveBox(BoxLayout):
    pass

class ParametresBox(BoxLayout):
    pass

class CentredTextInput(RelativeLayout):
    pass

class ThreeButton(BoxLayout):
    def __init__(self):
        self.premier = ObjectProperty(False)     
        self.deuxieme = ObjectProperty(True)     
        self.troisieme = ObjectProperty(False)   
#    premier = ObjectProperty(True)
 #   deuxieme = ObjectProperty(False)
  #  troisieme = ObjectProperty(False)
    def test1(self,instance):
        if self.premier is True :
            print("lepremier")
        if self.deuxieme is True:
            print("ledeuxieme")
        if self.troisieme is True:
            print("letroisieme")
            
            
class ButtonPlusMinus(BoxLayout):
    pass


class Application(BoxLayout):
    pass

class testApp(App):
        def build(self):
            self.title="Un putain de bon titre"
            return Application()

        
testapp = testApp()

testapp.run()
