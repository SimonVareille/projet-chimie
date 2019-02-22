# -*- coding: utf-8 -*-
from .graph_base import MainGraphBase
import matplotlib.pyplot as plt

class MainGraph(MainGraphBase):
    def __init__(self, t, I):
        MainGraphBase.__init__(self, t, I)
        self.fig, self.ax = plt.subplots()
       
    def update(self):
        self.ax.clear()
        self.ax.plot(self.t, self.I, label='Theoric')
        if self.displayExperimental:
            if self.expD != None:
                self.ax.plot(self.expt, self.expI,'r.', label='Expérimental\nD = {}'.format(self.expD) )
            else:
                self.ax.plot(self.expt, self.expI,'r.', label='Expérimental')

        self.ax.set_title("Cottrel Curve")
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Intensity (A)')
        self.ax.set_ylim(float(self.Ibottom), float(self.Itop), auto=True)
        self.ax.set_xlim(float(self.tleft), float(self.tright), auto=True)

        self.ax.legend()
        #self.fig.canvas.draw()

    def get_canvas(self):
        return self.fig.canvas
