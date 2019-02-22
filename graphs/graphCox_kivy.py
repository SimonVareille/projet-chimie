# -*- coding: utf-8 -*-
from kivy.garden.graph import Graph, MeshLinePlot
import cottrel.cox_math as Cox

class GraphCox:
    def __init__(self, x, t, D):
        self.x=x
        self.t=t
        self.D=D
        
        self.graph = Graph( xlabel='x', ylabel='Cox/Cox0', 
            x_ticks_minor=0.02, x_ticks_major=0.1, y_ticks_major=0.1, y_ticks_minor=0.02,
            y_grid_label=True, x_grid_label=True, padding=5,
            x_grid=False, y_grid=False, 
            xmin=0, xmax=0.3, ymin=0, ymax=1)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        
    def set_graph (self, x):
        self.x=x
        self.CoxQuotient=Cox.cox_curve(self.D, self.t, self.x)
       
    def update(self):
        self.plot.points = list(zip(self.x, self.CoxQuotient))
        self.graph.add_plot(self.plot)
            
    def get_canvas(self):
        return self.graph
