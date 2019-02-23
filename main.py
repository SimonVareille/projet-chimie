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
    
    import graphs.graph_matplot as maingraph
    import graphs.graphCox_matplot as coxgraph
else:
    import graphs.graph_kivy as maingraph
    import graphs.graphCox_kivy as coxgraph

if config.USE_NUMPY:
    import cottrel.cottrel_numpy as cottrel
    from linear_regression import LinearRegression
else:
    import cottrel.cottrel_math as cottrel

from data_reader import DataReader

import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock


class MainWindow(Widget):
    '''Classe représentant la fenêtre principale
    Elle a le même nom que dans app.kv.
    '''
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        
        self.t = cottrel.create_t(0, 20, 1000)
        self.I = cottrel.courbe_cottrel_th(1, 1, 10**-3, 10**(-5), self.t)
        
        reader = DataReader("experimental.csv")
        
        self.expt = reader.get_t()
        self.expI = reader.get_I()
        
        self.mainGraph = maingraph.MainGraph(self.t, self.I)
        
        self.mainGraph.set_experimental_data(self.expt, self.expI)
        self.mainGraph.display_experimental()
        self.mainGraph.set_limit_interval()
        
        linreg = LinearRegression(self.expt, self.expI)
        
        linreg.set_t_interval(1, 50)
        
        expD, coeff = linreg.regression(1, 1, 10**-3)
        
        self.mainGraph.set_expD(expD)
        
        self.mainGraph.update()
        
        self.ids.curveBoxLayout.add_widget(self.mainGraph.get_canvas())


class AppApp(App):
    '''L'application en elle même.
    '''
    def build(self):
        return MainWindow()
    
    def on_pause(self):
        return True


if __name__ in ('__main__', '__android__'):
    AppApp().run()
