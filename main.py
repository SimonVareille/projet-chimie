# -*- coding: utf-8 -*-

"""Ces deux prochaines lignes servent à dire à matplotlib d'utiliser le backend interactif de kivy.
Le backend est l'environnement de dessin (pour plus d'infos : https://matplotlib.org/tutorials/introductory/usage.html#what-is-a-backend
Il faut mettre ces deux lignes avant toute autre importation et déclaration de matplotlib.
Il est possible qu'on puisse le laisser dans ce main.py et que ça affectera les autres fichiers (ce qui serait le mieux pour du clean code),
mais c'est à tester.
"""
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

import kivy
kivy.require('1.0.7')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
#from kivy.garden.matplotlib.backend_kivy import FigureCanvas

"""----------------------------------Ici commence ce qu'il faut déplacer-------------------------------------"""
import matplotlib.pyplot as plt
import numpy as np

#Êplt.ion()

#np.random.seed(19680801)

"""Le générateur de la courbe de cottrel.
Dans l'absolue, t peut être n'importe quoi assimilable à
un nombre (on peut mettre un int ou un float, mais ici on met 
un np.linspace)
Retourne un nombre si t est un nombre, et une liste de nombre
si t est une liste de nombre.
"""
def courbeA(n, S, C, D, t):
    F = 96485.3329
    I = n*F*S*C*np.sqrt(D/np.pi)*np.sqrt(1/t)
    return I

t = np.linspace(0.00001, 20, 1000)
I = courbeA(1, 1,10**-3, 10**(-5), t)

"""Cette commande plt.subplots() est la base de l'affichage,
ax :    objet de type Axes (ou un tableau d'Axes, voir la doc)
        qui contient un graphique (pouvant contenir plusieurs courbes).
fig :   objet de type Figure qui contient les objets Axes,
        donc pouvant contenir plusieurs graphiques.
        C'est de lui que l'on obtient l'objet que l'on peut dessiner avec kivy.
"""
fig, ax = plt.subplots()
#fig, (ax, ax2) = plt.subplots(1, 2, sharey=True, sharex=True)
#ax2.scatter(t, I)

"""Fonction servant à recréer le graphique à chaque fois que l'on veux
(notamment pour le mettre à jour)
Note que l'on peut afficher plusieurs courbes sur un graphique en
appellant plusieurs fois ax.plot()
"""
def axUpdate(t, I):
    ax.plot(t, I, label='Theoric')
    ax.plot(t,I+30, label='Experimental')
    
    ax.set_title("Cottrel Evolution V3")
    ax.set_xlabel('time (s)')
    ax.set_ylabel('Intensity (A)')
    ax.set_ylim(0,50, auto=True)
    ax.set_xlim(0,20, auto=True)
    
    #Permet d'afficher une légende (le nom de chaque courbes)
    ax.legend()

"""----------------------------------Fin de ce qu'il faut déplacer-------------------------------------"""
#Première création du graphique
axUpdate(t,I)

#Récupération de l'objet à afficher (remarque: on peut l'afficher en faisant box.add_widget(canvas) comme ce qui est mis dans AppApp
canvas = fig.canvas

"""Classe représentant la fenêtre principale (de type BoxLayout 
pour qu'elle prenne toute la place qui lui est possible, mais
ça peut marcher avec d'autre types...)
Elle a le même nom que dans App.kv
"""
class MainWindow(BoxLayout):
    pass


#plt.show()

class AppApp(App):
    def build(self):
        self.mainWindow = MainWindow()
        self.i=1
        #self.box = BoxLayout()
        #self.box.add_widget(canvas)#FigureCanvas(fig))
        #canvas.draw()
        #Clock.schedule_interval(self.update, 1 / 60.)
        #return self.mainWindow#self.box
    def update(self, delta):
        I = courbeA(self.i, 1,10**-3, 10**(-5), t)
        ax.clear()
        axUpdate(t,I)
        canvas.draw()
        self.i+=1


if __name__ == '__main__':
    AppApp().run()
