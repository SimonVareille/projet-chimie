# -*- coding: utf-8 -*-

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
import os
import platform

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
            self.filechooser.path = "~/"
    
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