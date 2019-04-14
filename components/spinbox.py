# -*- coding: utf-8 -*-

import os

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout

from .entrypopup import EntryPopup
from .errorpopup import ErrorPopup


Builder.load_file(os.path.dirname(__file__) +'/spinbox.kv')

class SpinBox(BoxLayout):
    """
    Permet à l'utilisateur de rentrer une valeur sous la forme d'un bouton qui 
    ouvre un popup de saisie (via `EntryPopup`) et de boutons + et - permettant 
    d'ajouter ou de retrancher `steps` à la valeur saisie.
    Si l'utilisateur rentre une valeur invalide via `EntryPopop`, 
    un popup d'erreur (`ErrorPopup`) s'affiche (cf méthode `evaluation()`).
    """
    
    value = NumericProperty(1)
    min_value = NumericProperty(0)
    max_value = NumericProperty(100)
    buttonMid_id = ObjectProperty(None)

    steps = NumericProperty(0.1)
    
    _display_value = StringProperty("1")
    
    def __init__(self, **kwargs):
        super(SpinBox, self).__init__(**kwargs)
        
    def convert_to_scientific_notation(self,number):
        value_to_return=str(number)
        if len(value_to_return)>6:
            value_to_return="{:.3e}".format(number)
        return value_to_return

    def change_value_button(self, popup):
        value = self.evaluation(popup.returnValue)
        #Si value == "", self.value ne change pas de valeur.
        self.value = value if value is not None else self.value
         
        self._display_value = self.convert_to_scientific_notation(self.value)

    def opening_popup(self):
        entry_popup=EntryPopup()
        entry_popup.initValue = str(self.value)
        entry_popup.bind(on_dismiss=self.change_value_button)
        entry_popup.open()

    def add_one(self):
        #Augmente self.value par self.steps
        if not self.value:
            value = 0
        else:
            value = float(self.value)
         
        value += self.steps
        if value > self.max_value:
            value = self.max_value
        self.value = value
        self._display_value = self.convert_to_scientific_notation(self.value)
        
    def substract_one(self):
        #Diminue self.value par self.steps
        if not self.value:
            value = 0
        else:
            value = float(self.value)

        value -= self.steps
        if value < self.min_value:
            value = self.min_value
        self.value = value
        self._display_value = self.convert_to_scientific_notation(self.value)

    def ConvertToCalculate(self, string):
        return string.replace("^","**")

    def evaluation(self, entry):
        """Permet d'évaluer la valeur numérique d'une chaine de caractère et la
        retourne.
        Si l'evaluation via `eval()` aboutie à une erreur, un popup s'affiche avec
        un court texte pour l'utilisateur et la fonction retourne `None`.
        """
        #Import local, visible uniquement dans cette méthode.
        #On importe des fonctions pour permettre un eval("sqrt(10)")
        #par exemple. 
        from math import sqrt, pow, log, log10, cos, sin, tan

        if entry:
            try:
                toReturn=eval(self.ConvertToCalculate(entry))
                return(toReturn)
            except Exception as err:
                ErrorPopup("Erreur dans l'expression saisie.\nPar exemple : \n\
05 n'est pas reconnu comme 5\n++ n'est pas reconnu").open()
                return None
            
    def on_value(self, instance, value):
        self._display_value = self.convert_to_scientific_notation(value)
        
    def on__display_value(self, instance, value):
        pass
    









