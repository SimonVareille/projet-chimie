from kivy.uix.popup import Popup
from kivy.properties import  NumericProperty, ObjectProperty
from kivy.lang.builder import Builder

import os
Builder.load_file(os.path.dirname(__file__) + '/cox_popup.kv')

class CoxPopup(Popup):
    CoxvalDth=NumericProperty(10**(-5))
    CoxvalN=NumericProperty(1)
    CoxvalS=NumericProperty(0.25)
    CoxvalC=NumericProperty(10**(-5))