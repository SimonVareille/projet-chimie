# -*- coding: utf-8 -*-

import os
import platform

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock

from components.errorpopup import ErrorPopup

"""Adapté du site officiel de kivy (d'où les commentaires en anglais)
https://kivy.org/doc/stable/api-kivy.uix.filechooser.html
"""
Builder.load_file(os.path.dirname(__file__) +'/file_chooser.kv')

class OpenDialog(FloatLayout):
    """ Component to put inside another widget (in a popup for exemple).
    Display an interface to load files.
    
    Usage:
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    """
    
    filechooser = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(OpenDialog, self).__init__(**kwargs)
        
        #Prevent user to go through system directory on Android
        if platform.machine()=="armv8l":
            self.filechooser.rootpath = "/sdcard"
            self.filechooser.path = "/sdcard/Download"
        elif platform.system() == "Linux":
            self.filechooser.path = os.path.expanduser("~/")
        Clock.schedule_once(self.on_loaded)
        #self.filechooser.bind(on_parent=self.on_loaded)
    
    def on_loaded(self, *args, **kwargs):
        if not os.access(self.filechooser.path, os.R_OK):
            ErrorPopup(text="Vous n'avez pas les droits pour accéder au stockage !\n\
Veuillez autoriser l'appli à y accéder en passant par les paramètres.").open()
        
    load = ObjectProperty(None)
    ''' Function to call when the "Ouvrir" button is released.
    Must be defined as follow:
        my_func(path, filename)
    
    To set it, simply do: `loadDialog.load = my_func
    '''
    cancel = ObjectProperty(None)
    ''' Function to call when the "Annuler" button is released.
    Must be defined as follow:
        my_cancel()
    
    To set it, simply do: `loadDialog.load = my_cancel
    '''