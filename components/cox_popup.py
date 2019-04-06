from kivy.uix.popup import Popup
from kivy.properties import  NumericProperty, ObjectProperty
from kivy.lang.builder import Builder
#from ..graphs.graphCox_kivy import CoxGraph


import os
Builder.load_file(os.path.dirname(__file__) + '/cox_popup.kv')

class CoxPopup(Popup):
    
    grahCoxLayout=ObjectProperty(None)
    
    maxt=NumericProperty(200)
    mint=NumericProperty(1)
    
    CoxvalDth=NumericProperty(10**(-5))
    CoxvalN=NumericProperty(1)
    CoxvalS=NumericProperty(0.25)
    CoxvalC=NumericProperty(10**(-5))
    coxvalt=NumericProperty(1)
    
    
    def __init__(self, coxGraph, cox_curve, linspace):
        super(CoxPopup, self).__init__()
        
        
        
        self.coxGraph = coxGraph 
        self.cox_curve = cox_curve
        self.linspace=linspace
        
        self.xtab=self.linspace(0,200,1000)
        self.grahCoxLayout.add_widget(self.coxGraph.get_canvas())
        
        
    def on_slider_T_active(self):
        
        
        self.coxvalt=self.sliderCoxT.value
        self.coxGraph.x=self.xtab
        self.coxGraph.cox=self.cox_curve(self.CoxvalDth,self.coxvalt, self.xtab)
        self.coxGraph.update()


