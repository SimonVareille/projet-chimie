# -*- coding: utf-8 -*-

from kivy.properties import  StringProperty, NumericProperty

from kivy.uix.boxlayout import BoxLayout
from .entrypopup import EntryPopup
from kivy.lang.builder import Builder
import os
from .errorpopup import ErrorPopup

Builder.load_file(os.path.dirname(__file__) +'/intervalbox.kv')


class IntervalBox(BoxLayout):
    """
    Permet à l'utilisateur de rentrer les valeurs min et max de l'intervalle. 
    Ces valeurs sont stockées dans self.val_min et self.val_max.    
        Si l'utilisateur rentre une valeur invalide, un popup d'erreur (ErrorPopup)
    s'affiche (cf fonction evaluation()).
    """
    val_min=NumericProperty(0)#valeurs arbitraires
    _display_value_min=StringProperty("0")
    val_max=NumericProperty(100)
    _display_value_max=StringProperty("100")


    def update_display_val(self):
         self._display_value_min = self.convert_to_scientific_notation(self.val_min)
         self._display_value_max = self.convert_to_scientific_notation(self.val_max)
        
    def change_value_button_min(self, popup):
        value = self.evaluation(popup.returnValue)
        #Si value == "", self.value ne change pas de valeur.
        #Ce n'est peut-être pas le comportement attendu.
        self.val_min = value if value is not None else self.val_min
         
        self._display_value_min = self.convert_to_scientific_notation(self.val_min)
        #Si value est None, on ne ferme pas le popup. (On retourne True)        
        return value is None

    def opening_popup_min(self):
        entry_popup=EntryPopup()
        entry_popup.initValue = str(self.val_min)
        entry_popup.bind(on_dismiss=self.change_value_button_min)
        entry_popup.open()
        
        
        
        
    def change_value_button_max(self, popup):
        value = self.evaluation(popup.returnValue)
        #Si value == "", self.value ne change pas de valeur.
        #Ce n'est peut-être pas le comportement attendu.
        self.val_max = value if value is not None else self.val_max
         
        self._display_value_max = self.convert_to_scientific_notation(self.val_max)
        #Si value est None, on ne ferme pas le popup. (On retourne True)        

    def opening_popup_max(self):
        entry_popup=EntryPopup()
        entry_popup.initValue = str(self.val_max)
        entry_popup.bind(on_dismiss=self.change_value_button_max)
        entry_popup.open()
        
        
        
    def ConvertToCalculate(self, string):
        return string.replace("^","**")

    def evaluation(self, entry):
        """Permet d'évaluer la valeur numérique d'une chaine de caractère et la
        retourne.
        Si l'evaluation via eval() aboutit à une erreur, un popup s'affiche avec
        un court texte pour l'utilisateur et la fonction retourne None
        """
        from math import sqrt, pow, log, log10, cos, sin, tan
        #Import local, visible uniquement dans cette méthode.
        #On importe des fonctions pour permettre un eval("sqrt(10)")
        #par exemple. A mettre ou pas.
        if entry:
            try:
                toReturn=eval(self.ConvertToCalculate(entry))
                return(toReturn)
            except Exception as err:
                ErrorPopup("Erreur dans l'expression saisie.\nPar exemple : \n05 n'est pas reconnu comme 5\n++ n'est pas reconnu").open()
                return None
    def convert_to_scientific_notation(self,number):
        value_to_return=str(number)
        if len(value_to_return)>10:
            value_to_return="{:.3e}".format(number)
        return value_to_return

