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

class MyTextInput(RelativeLayout):

    def manage_input_filter(self, myTexte, from_undo=False):
        print("Test filter",self.myTexte.text)

    def read_value(self):
        print("Final value = ",self.myTexte.text)

    def read_instant_value(self):
        print("Value = ",self.myTexte.text)

 
class ButtonPlusMinus(BoxLayout):

    myTexte = ObjectProperty()

    def add_one(self):
        value = float(self.myTexte.text)
        value = round(value + 0.1, 2)
        self.myTexte.text = str(value)

    def substract_one(self):
        value = float(self.myTexte.text)
        if value <= 0:
            value = 0 
        else:
            value = round(value - 0.1, 2)
        self.myTexte.text = str(value)



class Application(BoxLayout):
    pass

class test47App(App):
        def build(self):
            self.title="Titre"
            return Application()

        
testapp = testApp()

testapp.run()
