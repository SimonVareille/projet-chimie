# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang.builder import Builder

import os
Builder.load_file(os.path.dirname(__file__) + '/entrypopup.kv')
"""
Dans l'idéal il faudrait modifier le fonctionnement de la classe pour qu'elle
prenne et renvoie des floats, mais il faudrait alors aussi modifier les 
endroits où on en fait l'appel (possibilité d'amélioration).
"""
class EntryPopup(Popup):
    """
    Cette fonction a pour but de permettre à l'utilisateur de saisir des 
    valeurs. Pour l'utiliser il faut initialiser initValue avec un str d'une 
    valeur numérique. 
    Pour récupérer la valeur de retour il faut utiliser
    bind(on_dismiss=*nomDeLaFonction*). 
    A ce moment là, la valeur de returnValue vaut initValue si on a fermé le
    popup sans passer par "OK" et la valeur rentrée par l'utilisateur si il a 
    été fermé avec "OK".
    
    """
    entry = ObjectProperty(None)
    returnValue = StringProperty(None)
    initValue = StringProperty(None)
    
    def __init__(self,**kwargs):
        super(EntryPopup, self).__init__(**kwargs)
        
    def on_open(self):
        super(EntryPopup, self).on_open()
        self.entry.text = ""
        self.returnValue = self.initValue        
    
    def on_ok_active(self):
        try:
            self.returnValue = self.entry.text
            self.dismiss()
        except Exception as err :
            self.returnValue = self.initValue
        
        
        