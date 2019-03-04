# -*- coding: utf-8 -*-
from kivy.garden.graph import Graph, SmoothLinePlot, DotPlot
from .graph_base import MainGraphBase

class MainGraph(MainGraphBase):
    """Cette classe crée le graphique principal en utilisant kivy.garden.graph.
    """
    def __init__(self, t, I):
        """
        """
        MainGraphBase.__init__(self, t, I)
        graph_theme = {
                'label_options': {
                    'color': [0, 0, 0, 1],  # color of tick labels and titles
                    'bold': False},
                'background_color': [1, 1, 1, 1],  # back ground color of canvas
                'tick_color': [0, 0, 0, 1],  # ticks and grid
                'border_color': [0, 0, 0, 1]}  # border drawn around each graph
                
        self.graph = Graph(title = 'Cottrel Curve',
                           xlabel='Time (s)',
                           ylabel='Intensity (A)', 
                           x_ticks_minor=5,
                           x_ticks_major=5,
                           y_ticks_major=0.2,
                           y_ticks_minor=5,
                           y_grid_label=True,
                           x_grid_label=True,
                           draw_border=True,
                           padding=5,
                           x_grid=False,
                           y_grid=False, 
                           xmin=float(self.tleft),
                           xmax=float(self.tright), 
                           ymin=float(self.Ibottom),
                           ymax=float(self.Itop),
                           **graph_theme)
        
        self.thplot = SmoothLinePlot(color=[0, 0, 1, 1])
        self.thplot.label = 'Theoric'
        self.graph.add_plot(self.thplot)
        
        self.expplot = DotPlot(color=[1, 0, 0, 1])
        self.expplot.label = 'Expérimental'
        self.expplot.point_size = 3
        self.graph.add_plot(self.expplot)
        
        self.graph.legend = False
            
    def update(self): 
        """Met à jour l'affichage.
        """
        if self._display_theoric:
            self.thplot.points = list(zip(self.t,self.I))
        else:
            self.thplot.points = list()
        if self._display_experimental:
            self.expplot.points = list(zip(self.expt,self.expI))
            if self.expD != None:
                self.expplot.label = 'Expérimental\nD = {}'.format(self.expD)
            else:
                self.expplot.label = 'Expérimental'
        else:
            self.expplot.points = list()
        self.graph.xmin = float(self.tleft)
        self.graph.xmax = float(self.tright)
        
        self.graph.ymin = float(self.Ibottom)
        self.graph.ymax = float(self.Itop)
            
    def get_canvas(self):
        return self.graph
