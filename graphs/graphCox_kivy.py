# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.garden.graph import Graph ,SmoothLinePlot
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

from kivymd.color_definitions import colors

class CoxGraph():
    """Crée le graphique contenant la courbe de Cox en utilisant 
    `kivy.garden.graph`.
    """
    
    def __init__(self, x=[], cox=[]):
        """
        Paramètres
        ----------
        x : list
            Tableau des distances à l'électrode.
        cox : list
            Tableau de la concentration.
        """
        self.x = x
        self.cox = cox

        theme_cls = App.get_running_app().theme_cls
        graph_theme={}
        if App.get_running_app().theme == 'default':
            graph_theme = {
                    'label_options': {
                        'color': [0, 0, 0, 1],  # color of tick labels and titles
                        'bold': False,
                        'markup': True},
                    'background_color': [1, 1, 1, 1],  # back ground color of canvas
                    'tick_color': [0, 0, 0, 1],  # ticks and grid
                    'border_color': [0, 0, 0, 1]}  # border drawn around each graph
        elif App.get_running_app().theme ==  'material-design':
            graph_theme = {
                    'label_options': {
                        'color': get_color_from_hex(colors[theme_cls.primary_palette][theme_cls.primary_hue]),#[0, 0, 0, 1],  # color of tick labels and titles
                        'bold': False,
                        'markup': True},
                    'background_color': get_color_from_hex(colors[theme_cls.theme_style]["Background"]),#[1, 1, 1, 1],  # back ground color of canvas
                    'tick_color': get_color_from_hex(colors[theme_cls.accent_palette][theme_cls.accent_hue]),#[0, 0, 0, 1],  # ticks and grid
                    'border_color': get_color_from_hex(colors[theme_cls.accent_palette][theme_cls.accent_hue])}#[0, 0, 0, 1]}  # border drawn around each graph
                
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
                           xmax=float(0.05), 
                           ymin=float(0),
                           ymax=float(1),
                           precision="%#.4g",
                           **graph_theme)
        
        self.coxplot = SmoothLinePlot(color=[0, 0, 1, 1])
        self.coxplot.label = "Concentration"

        self.graph.add_plot(self.coxplot)
        
        self._trigger = Clock.create_trigger(self.update_ticks)
        self.graph._plot_area.bind(pos=self._trigger)
        
    def update(self, *args): 
        """Met à jour l'affichage.
        """
        self.coxplot.points = list(zip(self.x,self.cox))

        self.graph.xmin = min(self.x)
        self.graph.xmax = max(self.x)
        
        self.update_ticks()
    
    def update_ticks(self, *args):
        """Met à jour l'échelle.
        """
        width, height = self.graph.get_plot_area_size()
        self.graph.x_ticks_major = (self.graph.xmax-self.graph.xmin)/(width/100)
        self.graph.x_ticks_minor = 10
        self.graph.y_ticks_major = (self.graph.ymax-self.graph.ymin)/(height/50)
        self.graph.y_ticks_minor = 5
        
    def get_canvas(self):
        return (self.graph)
