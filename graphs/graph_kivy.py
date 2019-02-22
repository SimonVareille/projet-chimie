# -*- coding: utf-8 -*-
from kivy.garden.graph import Graph, MeshLinePlot
from .graph_base import MainGraphBase

class MainGraph(MainGraphBase):
    """Cette classe crée le graphique principal en utilisant kivy.garden.graph.
    A compléter.
    """
    def __init__(self, t, I):
        MainGraphBase.__init__(self, t, I)
        self.graph = Graph(xlabel='Time (s)', ylabel='Intensity (A)', 
            x_ticks_minor=1, x_ticks_major=5, y_ticks_major=1,
            y_ticks_minor=0.05, y_grid_label=True, x_grid_label=True,
            padding=5, x_grid=False, y_grid=False, 
            xmin=float(self.tleft), xmax=float(self.tright), 
            ymin=float(self.Ibottom), ymax=float(self.Itop))
        print("Imax =",self.Itop)
            
    def update(self): 
        """Met à jour l'affichage.
        A compléter.
        """
        self.thplot = MeshLinePlot(color=[1, 0, 0, 1])
        self.thplot.points = list(zip(self.t,self.I))
        self.graph.add_plot(self.thplot)
        
        if self.displayExperimental:
            self.expplot = MeshLinePlot (color=[1,1,0,0])
            self.expplot.points = list(zip(self.expt,self.expI))
            self.graph.add_plot(self.expplot)
            
    def get_canvas(self):
        return self.graph
