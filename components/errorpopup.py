# -*- coding: utf-8 -*-
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder

import os
#Builder.load_file(os.path.dirname(__file__) + '/errorpopup.kv')

class ErrorPopup(Popup):
    """ Affiche un popup d'erreur.
    
    Utilisation :
        `ErrorPopup(text="Voici le texte d'erreur.").open()`
    """
    textid = ObjectProperty(None)
    
    def __init__(self,text):
        """
        Paramètres
        ----------
        text : str
            Texte à afficher.
        """
        super(ErrorPopup, self).__init__()
        self.textid.text = text

        