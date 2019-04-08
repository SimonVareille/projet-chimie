from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder



import os
Builder.load_file(os.path.dirname(__file__) + '/interval_popup.kv')

class IntervalPopup(Popup):
    intervalbox=ObjectProperty(None)

        