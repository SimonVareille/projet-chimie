# -*- coding: utf-8 -*-

import os

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder

#Builder.load_file(os.path.dirname(__file__) + '/interval_popup.kv')

class IntervalPopup(Popup):
    """Popup affichant la sélection d'intervalle.
    """
    intervalbox=ObjectProperty(None)

        