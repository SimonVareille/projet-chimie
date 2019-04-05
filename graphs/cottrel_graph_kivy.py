# -*- coding: utf-8 -*-
from kivy.garden.graph import Graph, SmoothLinePlot, DotPlot
from .cottrel_graph_base import CottrelGraphBase
import math

class CottrelGraph(CottrelGraphBase):
    """Cette classe crée le graphique contenant les courbes de Cottrel en 
    utilisant kivy.garden.graph.
    """
    def __init__(self, t=[], I=[]):
        """
        """
        super(CottrelGraph, self).__init__(t, I)
        graph_theme = {
                'label_options': {
                    'color': [0, 0, 0, 1],  # color of tick labels and titles
                    'bold': False},
                'background_color': [1, 1, 1, 1],  # back ground color of canvas
                'tick_color': [0, 0, 0, 1],  # ticks and grid
                'border_color': [0, 0, 0, 1]}  # border drawn around each graph
                
        self.graph = Graph(title = 'Courbes de Cottrel',
                           xlabel='Temps (s)',
                           ylabel='Intensité (A)',
                           x_ticks_minor=5,
                           x_ticks_major=5,
                           y_ticks_major=0.2,
                           y_ticks_minor=4,
                           y_grid_label=True,
                           x_grid_label=True,
                           padding=5,
                           x_grid=False,
                           y_grid=False, 
                           xmin=float(self.tleft),
                           xmax=float(self.tright), 
                           ymin=float(self.Ibottom),
                           ymax=float(self.Itop),
                           **graph_theme)
        
        self.thplot = SmoothLinePlot(color=[0, 0, 1, 1])
        self.thplot.label = "Théorique"
        
        self.expplot = SmoothLinePlot(color=[1, 0, 0, 1])
        self.expplot.label = "Expérimentale"
        
#        self.testplot = SmoothLinePlot(color=[0, 1, 0, 1])
#        self.testplot.points = [(5,0), (5,1.2)]
#        self.graph.add_plot(self.testplot)
        
        self.graph.legend = True
            
    def update(self): 
        """Update the graph. Redraw the widgets.
        """
        if self._display_theoric:
            self.thplot.points = list(zip(self.t,self.I))
            if self.thplot not in self.graph.plots:
                self.graph.add_plot(self.thplot)
        else:
            if self.thplot in self.graph.plots:
                self.graph.remove_plot(self.thplot)
                
        if self._display_experimental:                
            self.expplot.points = list(zip(self.expt,self.expI))
            if self.expD != None:
                self.expplot.label = 'Expérimentale\nD = {}'.format(self.expD)
            else:
                self.expplot.label = 'Expérimentale'
            
            if self.expplot not in self.graph.plots:
                self.graph.add_plot(self.expplot)
        else:
            if self.expplot in self.graph.plots:
                self.graph.remove_plot(self.expplot)
                
        self.graph.xmin = float(self.tleft)
        self.graph.xmax = float(self.tright)
        
        self.graph.ymin = float(self.Ibottom)
        self.graph.ymax = float(self.Itop) if self.Ibottom!=self.Itop else 1.0
            
    def get_canvas(self):
        return self.graph
    
    def to_widget(self, x, y, relative=False):
        return self.graph.to_widget(x, y, relative)
    
    def zoom(self, dx, dy, cx, cy):
        """
        Zoom into the graph by a factor.
        
        Set dx or dy over 1 zoom into the graph and below 1 it dezoom.
        Default is dx=1, dy=1
        
        Parameters
        ----------
        dx : real
            horizontal zoom factor
        dy : real
            vertical zoom factor
        center : tuple(x,y)
            Center of the zoom. Must be in widget coordinates.
            Convert from window coordinates with:
                `x, y = self.to_widget(x, y, relative=True)`
        """
        cx, cy = self.graph.to_data(cx, cy)
        range
        (cx - self.tleft)/(self.tright - self.tleft)
        (self.tright - cx)/(self.tright - self.tleft)
        tleft = cx - 0.5*(self.tright - self.tleft)/dx
        tright = tleft + (self.tright - self.tleft)/dx
        
        Ibottom = cy - 0.5*(self.Itop - self.Ibottom)/dy
        Itop = Ibottom + (self.Itop - self.Ibottom)/dy
        
        print(cx, cy)
        
        self.set_limit_interval(tleft, tright, Ibottom, Itop)
        self.update()
