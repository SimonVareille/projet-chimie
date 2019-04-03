from kivy.uix.popup import Popup
from kivy.properties import  NumericProperty, ObjectProperty
from kivy.lang.builder import Builder
from .intervalbox import IntervalBox



import os
Builder.load_file(os.path.dirname(__file__) + '/interval_popup.kv')

class IntervalPopup(Popup):
    intervalbox=ObjectProperty(None)

        