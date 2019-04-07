from kivy.uix.popup import Popup
from kivy.properties import  NumericProperty, ObjectProperty, StringProperty
from kivy.lang.builder import Builder
#from ..graphs.graphCox_kivy import CoxGraph


import os
Builder.load_file(os.path.dirname(__file__) + '/cox_popup.kv')

class CoxPopup(Popup):
    
    grahCoxLayout=ObjectProperty(None)
    
    maxt=NumericProperty(300)
    mint=NumericProperty(1)
    step=NumericProperty(1)
    
    CoxvalDth=NumericProperty(10**(-5))
    CoxvalN=NumericProperty(1)
    CoxvalS=NumericProperty(0.25)
    CoxvalC=NumericProperty(10**(-2))
    coxvalt=NumericProperty(20)
    _coxvaltToDisplay=StringProperty("20")
    
    def __init__(self, coxGraph, cox_curve, linspace):
        super(CoxPopup, self).__init__()
        
        
        
        self.coxGraph = coxGraph()
        self.cox_curve = cox_curve
        self.linspace=linspace
        
        self.xtab=self.linspace(0,0.1,200)
        
        
        self.grahCoxLayout.add_widget(self.coxGraph.get_canvas())
        
        
        self.on_slider_T_active()
        
        
    def on_slider_T_active(self):
        
        
        self.coxvalt=self.sliderCoxT.value
        self.coxGraph.x=self.xtab
        self.coxGraph.cox=self.cox_curve(self.CoxvalDth,self.coxvalt, self.xtab)
        self.coxGraph.update()
        self._coxvaltToDisplay = str(self.coxvalt)
#        self._coxvaltToDisplay = self.convert_to_display_notation(self.coxvalt)
        
    def convert_to_display_notation(self,number):
        value_to_return=str(number)
        value_to_return.replace("^","**")
        if len(value_to_return)>10:
            value_to_return="{:.4e}".format(number)
        return value_to_return
        

