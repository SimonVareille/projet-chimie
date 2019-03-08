# -*- coding: utf-8 -*-
from .cottrel_graph_base import CottrelGraphBase
import matplotlib.pyplot as plt

class CottrelGraph(CottrelGraphBase):
    """Cette classe crée le graphique contenant les courbes de Cottrel en 
    utilisant matplotlib.
    """
    def __init__(self, t, I):
        """
        """
        super(CottrelGraph, self).__init__(t, I)
        self.fig, self.ax = plt.subplots()
       
    def update(self):
        """Met à jour l'affichage.
        """
        self.ax.clear()
        if self._display_theoric:
            self.ax.plot(self.t, self.I, label='Theoric')
        if self._display_experimental:
            if self.expD != None:
                self.ax.plot(self.expt, self.expI,'r.', label='Experimental\nD = {}'.format(self.expD) )
            else:
                self.ax.plot(self.expt, self.expI,'r.', label='Experimental')

        self.ax.set_title("Cottrel Curve")
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Intensity (A)')
        self.ax.set_ylim(float(self.Ibottom), float(self.Itop), auto=True)
        self.ax.set_xlim(float(self.tleft), float(self.tright), auto=True)

        self.ax.legend()
        self.fig.canvas.draw()

    def get_canvas(self):
        return self.fig.canvas
