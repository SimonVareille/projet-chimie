# -*- coding: utf-8 -*-
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from kivy.uix.boxlayout import BoxLayout
from .popup import EntryPopup
from kivy.lang.builder import Builder
import os

Builder.load_file(os.path.dirname(__file__) +'/spinbox.kv')

class SpinBox(BoxLayout):
    value = NumericProperty(1)
    min_value = NumericProperty(0)
    max_value = NumericProperty(100)
    buttonMid_id = ObjectProperty(None)

    steps = NumericProperty(0.1)
    
    _display_value = StringProperty("1")
    
    def __init__(self, **kwargs):
        super(SpinBox, self).__init__(**kwargs)

    def TheFunction2(self, popup):
        value = self.evaluation(popup.entry.text)
        #Si value == "", self.value ne change pas de valeur.
        #Ce n'est peut-être pas le comportement attendu.
        self.value = value if value is not None else self.value
         
        self._display_value = str(self.value)
        #Si value est None, on ne ferme pas le popup. (On retourne True)
        return value is None

    def TheFunction(self):
        entry_popup=EntryPopup()
        entry_popup.entry.text = str(self.value)
        entry_popup.bind(on_dismiss=self.TheFunction2)
        entry_popup.open()

    def add_one(self):
        #Increase the value by 0.1
        if not self.value:
            value = 0
        else:
            value = float(self.value)
         
        value += self.steps
        if value > self.max_value:
            value = self.max_value
        self.value = value
        self._display_value = str(self.value)
    def substract_one(self):
        #Decrease the value by 0.1
        if not self.value:
            value = 0
        else:
            value = float(self.value)

        value -= self.steps
        if value < self.min_value:
            value = self.min_value
        self.value = value
        self._display_value = str(value)

    def ConvertToCalculate(self, string):
        return string.replace("^","**")

    def evaluation(self, entry):
        from math import sqrt, pow, log, log10, cos, sin, tan
        #Import local, visible uniquement dans cette méthode.
        #On importe des fonctions pour permettre un eval("sqrt(10)")
        #par exemple. A mettre ou pas.
        if entry:
            try:
                toReturn=eval(self.ConvertToCalculate(entry))
                print(toReturn)
                return(toReturn)
            except Exception as err:
                print(err)
                return None
            
    def on_value(self, instance, value):
        self._display_value = str(value)
        
    def on__display_value(self, instance, value):
        pass