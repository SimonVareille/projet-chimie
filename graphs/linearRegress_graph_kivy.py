# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 19:25:47 2019

@author: paula
"""

from linear_regression import LinearRegression
from kivy.garden.graph import Graph, SmoothLinePlot, DotPlot
from math import log

class GraphLinearRegression(LinearRegression):
    
    def __init__(self, n, S, C, t, I):
        super(GraphLinearRegression, self).__init__(t, I)
        self.n=n 
        self.S=S
        self.C=C
      
        self.logexp_and_linear_curves_tab(self.t, self.I)
        
        self.logtleft=float(min(self.logexpt)) #len(self.logexpt)-2
        self.logtright=float(max(self.logexpt))
        self.logIbottom=float(min(self.logexpI))
        self.logItop=float(max(self.logexpI))

        graph_theme = {
            'label_options': {
                'color': [0, 0, 0, 1],  # color of tick labels and titles
                'bold': False},
            'background_color': [1, 1, 1, 1],  # back ground color of canvas
            'tick_color': [0, 0, 0, 1],  # ticks and grid
            'border_color': [0, 0, 0, 1]}  # border drawn around each graph
            
        self.graph = Graph(title = 'Courbes de Regression lineaire',
           xlabel='log Temps (s)',
           ylabel='log Intensité (A)',
           x_ticks_minor=5,
           x_ticks_major=5,
           y_ticks_major=0.2,
           y_ticks_minor=4,
           y_grid_label=True,
           x_grid_label=True,
           padding=5,
           x_grid=False,
           y_grid=False, 
           xmin=self.logtleft,
           xmax=self.logtright, 
           ymin=self.logIbottom,
           ymax=self.logItop,
           **graph_theme)
    
        self.logexpplot = SmoothLinePlot(color=[0, 0, 1, 1])
        self.logexpplot.label = "Expérimentale"
        
        self.linlogexpplot = SmoothLinePlot(color=[1, 0, 0, 1])
        linearcoefficient, intercept= self.linregress()
        self.Dexp=self.calculate_D ( intercept, self.n, self.S, self.C)
        
        self.linlogexpplot.label = "Régression lineaire\nD="+str(self.Dexp)

        self.graph.legend = True
        
        self.set_graph ( self.logexpt, self.logexpI, self.linlogexpI)
        
        self.set_limit_interval(self.logtleft, self.logtright, self.logIbottom, self.logItop)
    
    def set_graph (self, logexpt, logexpI, linlogexpI):
        self.logexpplot.points = list(zip(logexpt, logexpI))
        self.linlogexpplot.points = list (zip(logexpt, linlogexpI))
        
        self.graph.add_plot(self.logexpplot) 
        self.graph.add_plot(self.linlogexpplot)     

        #les 4 suivants sont-ils utilent? a quoi servent-ils?
        
#        self.graph.xmin=float(log(self.t[self.indicetMin]))
    
#        self.graph.xmax=float(log(self.t[self.indicetMax]))

#        self.graph.ymin=float(log(min(self.I)))

#        self.graph.ymax=float(log(max(self.I)))
        
    def get_canvas(self):
        return self.graph

    def set_limit_interval(self, logtleft=None, logtright=None, logIbottom=None, logItop=None):
    
    
            width, height = self.graph.get_plot_area_size()
    
            self.graph.x_ticks_major = (self.logtright-self.logtleft)/(width/100)
    
            self.graph.x_ticks_minor = 10
    
            self.graph.y_ticks_major = (self.logItop-self.logIbottom)/(height/50)
    
            self.graph.y_ticks_minor = 5
