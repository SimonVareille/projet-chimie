# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder

import os
Builder.load_file(os.path.dirname(__file__) + '/popup.kv')

class EntryPopup(Popup):
    entry = ObjectProperty(None)