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

from kivy.config import Config
#Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button


class MainWindow(Widget):
    '''Classe représentant la fenêtre principale
    Elle a le même nom que dans app.kv.
    '''
    curveBoxLayout = ObjectProperty(None)
    expCurveSwitch = ObjectProperty(None)
    expCurveText = StringProperty("[color=ff3399]Courbe\n experimentale[/color]")
    
    buttonDth = ObjectProperty(None)
    buttonN = ObjectProperty(None)
    buttonS = ObjectProperty(None)
    buttonC = ObjectProperty(None)
    
    valDth=NumericProperty(None)
    valN=NumericProperty(None)
    valS=NumericProperty(None)
    valC=NumericProperty(None)


    
    thCurveSwitchActive = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        
        reader = DataReader("experimental.csv")
        
        self.expt = reader.get_t()
        self.expI = reader.get_I()
        
        if self.expt:
            self.t = cottrel.create_t(0, max(self.expt), 1000)
        else:
            self.t = cottrel.create_t(0, 20, 1000)
        self.I = cottrel.courbe_cottrel_th(1, 1, 10**-3, 10**(-5), self.t)
        
        self.mainGraph = cottrel_graph.CottrelGraph(self.t, self.I)
        
        self.mainGraph.set_experimental_data(self.expt, self.expI)
        self.mainGraph.display_experimental()
        
        self.mainGraph.set_limit_interval()
        
        if config.USE_NUMPY:
            linreg = LinearRegression(self.expt, self.expI)
            
            linreg.set_t_interval(1, 50)
            
            expD, coeff = linreg.regression(1, 1, 10**-3)
            
            self.mainGraph.set_expD(expD)
        
        self.mainGraph.update()
        
        self.curveBoxLayout.add_widget(self.mainGraph.get_canvas())
    
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
        
    def on_buttonparametre_active(self,instance):
        self.valDth=self.buttonDth.value
        self.valN=self.buttonN.value
        self.valC=self.buttonC.value
        self.valS=self.buttonS.value
        self.I = cottrel.courbe_cottrel_th(self.valN,self.valS, self.valC, self.valDth, self.t)
        self.mainGraph.I=self.I
        self.mainGraph.update()
    
    

class AppApp(App):
    '''L'application en elle même.
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
            popup = Popup(title = "Fermer ?", content=content, auto_dismiss=True, size_hint=(None, None), size=(400, 200))
            
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
