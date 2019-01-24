# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import numpy as np
from kivy.garden.matplotlib.backend_kivy import FigureCanvas

import matplotlib.pyplot as plt

#Êplt.ion()

#np.random.seed(19680801)

def courbeA(n, S, C, D, t):
    F = 96485.3329
    I = n*F*S*C*np.sqrt(D/np.pi)*np.sqrt(1/t)
    return I

t = np.linspace(0.00001, 20, 1000)
I = courbeA(1, 1,10**-3, 10**(-5), t)

fig, ax = plt.subplots()
#fig, (ax, ax2) = plt.subplots(1, 2, sharey=True, sharex=True)
#ax2.scatter(t, I)
def axUpdate(t, I):
    ax.plot(t, I, label='Theoric')
    ax.plot(t,I+30, label='Experimental')
    
    ax.set_title("Cottrel Evolution V3")
    ax.set_xlabel('time (s)')
    ax.set_ylabel('Intensity (A)')
    ax.set_ylim(0,50, auto=True)
    ax.set_xlim(0,20, auto=True)
    
    ax.legend()
    
axUpdate(t,I)
canvas = fig.canvas


#plt.show()

class MyApp(App):
    def build(self):
        self.i=1
        self.box = BoxLayout()
        self.box.add_widget(canvas)#FigureCanvas(fig))
        #canvas.draw()
        Clock.schedule_interval(self.update, 1 / 60.)
        return self.box
    def update(self, delta):
        I = courbeA(self.i, 1,10**-3, 10**(-5), t)
        ax.clear()
        axUpdate(t,I)
        canvas.draw()
        self.i+=1


if __name__ == '__main__':
    MyApp().run()
