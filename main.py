# -*- coding: utf-8 -*-

"""Pour la compatibilité avec python2"""
from __future__ import division

import config

"""On gère ici les modules que l'on veut importer (en fonction de ce qui est
 disponible).
"""
if config.USE_MATPLOTLIB:
    """Ces deux prochaines lignes servent à dire à matplotlib d'utiliser le backend
    interactif de kivy.
    Le backend est l'environnement de dessin (pour plus d'infos : 
    https://matplotlib.org/tutorials/introductory/usage.html#what-is-a-backend
    Il faut mettre ces deux lignes avant toute autre importation et déclaration de
    matplotlib.
    """
    import matplotlib
    matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
    
    import graphs.cottrel_graph_matplot as cottrel_graph
    import graphs.graphCox_matplot as coxgraph
else:
    import graphs.cottrel_graph_kivy as cottrel_graph
    import graphs.graphCox_kivy as coxgraph

if config.USE_NUMPY:
    import cottrel.cottrel_numpy as cottrel
    from linear_regression import LinearRegression
else:
    import cottrel.cottrel_math as cottrel

from data_reader import DataReader

import kivy
kivy.require('1.10.1')

import os

from kivy.config import Config
#Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, \
    NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from components.file_chooser import OpenDialog

from components.cox_popup import CoxPopup

from components.interval_popup import IntervalPopup






class MainWindow(Widget):
    '''Classe représentant la fenêtre principale
    Elle a le même nom que dans app.kv.
    '''
    curveBoxLayout = ObjectProperty(None)
    expCurveSwitch = ObjectProperty(None)

    #valeurs pour Dth
    buttonDth = ObjectProperty(None)    
    valDth=NumericProperty(10**(-5))
    valMinDth=NumericProperty(0)
    valMaxDth=NumericProperty(10**(-4))
    stepsDth=NumericProperty(10**(-6))
    
    #valeurs pour N
    buttonN = ObjectProperty(None)
    valN=NumericProperty(1)
    valMinN=NumericProperty(1)
    valMaxN=NumericProperty(4)
    stepsN=NumericProperty(1)

    #valeurs pour S
    buttonS = ObjectProperty(None)
    valS=NumericProperty(0.25)
    valMinS=NumericProperty(0)
    valMaxS=NumericProperty(0.5)
    stepsS=NumericProperty(0.01)
    
    #valeurs pour C
    buttonC = ObjectProperty(None)
    valC=NumericProperty(10**(-5))
    valMinC=NumericProperty(0)
    valMaxC=NumericProperty(1)
    stepsC=NumericProperty(10**(-6))
    
    sliderDth=ObjectProperty(None)
    
    thCurveSwitchActive = BooleanProperty(True)
    
    valIntervalMin=NumericProperty(0)
    valIntervalMax=NumericProperty(100)
    

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        
        #Valeurs pour Dth
        self.buttonDth.value=self.valDth
        self.buttonDth.min_value=self.valMinDth
        self.buttonDth.max_value=self.valMaxDth
        self.buttonDth.steps=self.stepsDth
        self.init_slider_Dth()
        
        #Valeurs pour N
        self.buttonN.value=self.valN
        self.buttonN.min_value=self.valMinN
        self.buttonN.max_value=self.valMaxN
        self.buttonN.steps=self.stepsN
    
        #Valeurs pour S
        self.buttonS.value=self.valS
        self.buttonS.min_value=self.valMinS
        self.buttonS.max_value=self.valMaxS
        self.buttonS.steps=self.stepsS
        
        #Valeurs pour C
        self.buttonC.value=self.valC
        self.buttonC.min_value=self.valMinC
        self.buttonC.max_value=self.valMaxC
        self.buttonC.steps=self.stepsC

        self.mainGraph = cottrel_graph.CottrelGraph()

        
        self.load_exp_data("", "experimental.csv")
        
        if self.expt:
            self.t = cottrel.create_t(0, max(self.expt), 1000)
        else:
            self.t = cottrel.create_t(0, 20, 1000)
        self.I = cottrel.courbe_cottrel_th(self.buttonN.value, self.buttonS.value, self.buttonC.value, self.buttonDth.value, self.t)
        
        
        self.mainGraph.set_experimental_data(self.expt, self.expI)
        self.mainGraph.display_experimental()
        
        self.mainGraph.set_limit_interval()
        
        self.linear_regression()
        
        self.mainGraph.update()
        
        self.curveBoxLayout.add_widget(self.mainGraph.get_canvas())
        
        self.bind_on_buttonparametre_active(self.buttonDth)
        self.bind_on_buttonparametre_active(self.buttonN)
        self.bind_on_buttonparametre_active(self.buttonS)
        self.bind_on_buttonparametre_active(self.buttonC)
                
        
        
        


    
    def on_expCurveSwitch_active(self, active):
        if active:
            self.mainGraph.display_experimental()
            self.mainGraph.set_limit_interval()
        else:
            self.mainGraph.display_experimental(False)
            self.mainGraph.set_limit_interval()
        self.mainGraph.update()
    
    def on_thCurveSwitch_active(self, active):
        if active:
            self.mainGraph.display_theoric()
            self.mainGraph.set_limit_interval()
        else:
            self.mainGraph.display_theoric(False)
            self.mainGraph.set_limit_interval()
        self.mainGraph.update()
    def on_buttonparametre_active(self,instance,text):
        '''met à jour la courbe avec les nouvelles valeurs'''
        self.valDth=self.buttonDth.value
        self.sliderDth.value=self.buttonDth.value
        self.valN=self.buttonN.value
        self.valC=self.buttonC.value
        self.valS=self.buttonS.value
        self.I = cottrel.courbe_cottrel_th(self.valN,self.valS, self.valC, self.valDth, self.t)
        self.mainGraph.I=self.I
        self.mainGraph.update()

    def bind_on_buttonparametre_active(self, spinbox):
        spinbox.buttonMid_id.bind(text = self.on_buttonparametre_active)
    
    def init_slider_Dth(self):
        self.sliderDth.min=self.buttonDth.min_value
        self.sliderDth.max=self.buttonDth.max_value
        self.sliderDth.value=self.buttonDth.value
        self.sliderDth.step=self.buttonDth.steps
    
    def on_slider_Dth_active(self):
        self.buttonDth.value=self.sliderDth.value
        

    def show_openDialog(self):
        '''Show a dialog in order to select the data file to open.
        '''
        content = OpenDialog()
        self._openPopup = Popup(title="Sélectionnez le fichier de données :", content=content,
                            size_hint=(0.9, 0.9))
        content.cancel = self._openPopup.dismiss
        content.load = self.load_data_from_dialog
        self._openPopup.open()
    
    def load_data_from_dialog(self, path, filename):
        if self.load_exp_data(path, filename):
            self._openPopup.dismiss()
    
    def load_exp_data(self, path, filename):
        '''Load the experimental data from file named `filename` located in 
        `path`. If `filename` is a list or a tuple, only the first cell is
        considered.
        '''
        if isinstance(filename, (list, tuple)):
            filename = filename[0]
        reader = DataReader(os.path.join(path, filename))
        
        self.expt = reader.get_t()
        self.expI = reader.get_I()
        
        self.mainGraph.set_experimental_data(self.expt, self.expI)
        
        #Recalculate the theoric value so that it fit the experimental range.
        self.t = cottrel.create_t(0, max(self.expt), 1000)
        self.I = cottrel.courbe_cottrel_th(self.valN, self.valS, self.valC, self.valDth, self.t)
        self.mainGraph.set_theoric_data (self.t, self.I)
        
        self.linear_regression()
        
        self.mainGraph.update()
        
        return True
    
    def linear_regression(self):
        '''Do the linear regression on the current experimental data and notify
        the mainGraph that the value has to be updated.
        '''
        if config.USE_NUMPY:
            linreg = LinearRegression(self.expt, self.expI)
            
            linreg.set_t_interval(1, 50)
            
            expD, coeff = linreg.regression(1, 1, 10**-3)
            
            self.mainGraph.set_expD(expD)
            
            
    def on_cox_button_active(self,instance):
        
        cox_popup=CoxPopup()
        cox_popup.CoxvalDth=self.valDth
        cox_popup.CoxvalS=self.valS
        cox_popup.CoxvalC=self.valC
        cox_popup.CoxvalN=self.valN
        cox_popup.open()
        
    def on_interval_define_button_active(self,instance):        
        interval_popup=IntervalPopup() 
        
        interval_popup.bind(on_dismiss=self.on_interval_popup_closed)
        interval_popup.open()
    
    def on_interval_popup_closed(self, popup):
        self.valIntervalMin=popup.intervalbox.val_min
        self.valIntervalMax=popup.intervalbox.val_max
        

    







class AppApp(App):
    '''The app itself.
    '''
    title = "Cottrel"
    def build(self):
        Window.bind(on_keyboard=self.key_input)
        return MainWindow()
    
    def on_pause(self):
        return True
    
    def on_resume(self):
        return True
    
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            content = BoxLayout(orientation = 'vertical')
            content.add_widget(Label(text = "Voulez vous vraiment fermer l'application ?"))
            
            buttons = BoxLayout(orientation = 'horizontal')
            button_close = Button(text='Fermer')
            button_cancel = Button(text='Annuler')
            buttons.add_widget(button_close)
            buttons.add_widget(button_cancel)
            
            content.add_widget(buttons)
            popup = Popup(title = "Fermer ?", content=content, auto_dismiss=True, size_hint=(0.3, 0.2))
            
            # bind the on_press event of the button to the dismiss function
            button_cancel.bind(on_press=popup.dismiss)
            button_close.bind(on_press=popup.dismiss)
            button_close.bind(on_press = self.close)
            
            # open the popup
            popup.open()
            return True  
        else:           # the key now does nothing
            return False
    
    def close(self, *args, **kwargs):
        Window.close()
        App.get_running_app().stop()


if __name__ in ('__main__', '__android__'):
    AppApp().run()
