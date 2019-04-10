# -*- coding: utf-8 -*-
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder

import os
Builder.load_file(os.path.dirname(__file__) + '/errorpopup.kv')

class ErrorPopup(Popup):
    """ Cette classe a pour but d'afficher un popup d'erreur avec le texte 
    donné en paramètre. Pour lancer le popup il faut lancer la fonction open() 
    de l'objet.
    """
    textid = ObjectProperty(None)
    
    
    def __init__(self,text):
        super(ErrorPopup, self).__init__()
        self.textid.text = text

        