# -*- coding: utf-8 -*-
from kivy.garden.graph import Graph, MeshLinePlot,SmoothLinePlot
import cottrel.cox_math as Cox

class CoxGraph():
    """Cette classe crée le graphique contenant les courbes de Cox en 
    utilisant kivy.garden.graph.
    """
    
    def __init__(self, x=[], cox=[]):
        self.x=x
        self.cox=cox

        graph_theme = {
                'label_options': {
                    'color': [0, 0, 0, 1],  # color of tick labels and titles
                    'bold': False,
                    'markup': True},
                'background_color': [1, 1, 1, 1],  # back ground color of canvas
                'tick_color': [0, 0, 0, 1],  # ticks and grid
                'border_color': [0, 0, 0, 1]}  # border drawn around each graph
                
        self.graph = Graph(title = 'Courbe C[sub]ox[/sub]',
                           xlabel='x',

                           ylabel='C[sub]ox[/sub] / C[sup]*[/sup] [sub]ox[/sub]',
                           x_ticks_minor=5,
                           x_ticks_major=5,
                           y_ticks_major=1,
                           y_ticks_minor=4,
                           y_grid_label=True,
                           x_grid_label=True,

                           padding=5,
                           x_grid=False,
                           y_grid=False, 
                           xmin=float(0),
                           xmax=float(1), 
  #                         ymin=float(0),
   #                        ymax=float(1),
                           **graph_theme)
        
        self.coxplot = SmoothLinePlot(color=[0, 0, 1, 1])
        self.coxplot.label = "Concentration"

        self.graph.add_plot(self.coxplot)
        

    def update(self): 
        """Met à jour l'affichage.
        """

        self.coxplot.points = list(zip(self.x,self.cox))

        self.set_limit_interval(min(self.x), max(self.x), min(self.cox), max(self.cox))

        self.graph.xmin = min(self.x)
        self.graph.xmax = max(self.x)

            
    def get_canvas(self):
        return self.graph



