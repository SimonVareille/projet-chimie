# -*- coding: utf-8 -*-
import matplotlib as plt
import cottrel.cox_math as Cox

class GraphCox:
    def __init__(self, x, t, D):
        self.x=x
        self.t=t
        self.D=D
        self.fig, self.ax = plt.subplots()  
        self.CoxQuotient=Cox.cox_curve( self.D,  self.t, self.x)
        
    def set_graph (self, x):
        self.x=x
        self.CoxQuotient=Cox.cox_curve( self.D, self.t, self.x)
        
    def update(self):
        self.ax.clear()
        self.ax.plot(self.x, self.CoxQuotient)
        
        self.ax.set_title("Evolution du profil de concentration")
        self.ax.set_xlabel('x (cm)')
        self.ax.set_ylabel('Cox/Cox0')
        self.ax.set_ylim(0, 1, auto=True)
        self.ax.set_xlim(0, 0.3, auto=True)
        
        self.ax.legend()

    def get_canvas(self):
        return self.fig.canvas
