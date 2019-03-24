# -*- coding: utf-8 -*-

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
import os

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