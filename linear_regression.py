# -*- coding: utf-8 -*-

"""Pour la compatibilité avec python2"""

from __future__ import division

import math as m

def liste_transformation_log (liste):
    loglist=list()
    for i in range (len(liste)):
        loglist.append(m.log(liste[i]))   
    return (loglist)

class LinearRegression:

    """Cette classe permet d'effectuer la régression linéaire sur les valeurs 
    expérimentales.
    """

    def __init__(self, t, I):
        self.t=t
        self.I=I
        self.tMin=t[0]
        self.tMax=t[-1]
        self.indicetMin=0
        self.indicetMax=len(t)-1

    def set_t_interval(self, tMin=None, tMax=None):

        """Sélectionne l'intervalle dans lequel on veut effectuer la régression
        linéaire.

        Paramètres
        ----------
        tMin : réel
            Valeur minimale de `t`. La valeur effectivement prise en compte est
            la plus proche valeur supèrieure ou égale à `tMin` présente dans le
            tableau `t`.
            Si `tMin` est None, `tMin` prend la plus petite valeur de `t`.
        tMax : réel
            Valeur maximale de `t`. La valeur effectivement prise en compte est
            la plus proche valeur infèrieure ou égale à `tMax` présente dans le
            tableau `t`.
            Si `tMax` est None, `tMax` prend la plus grande valeur de `t`.
        """

        if tMin == None:
            tMin = self.t[0]
        if tMax == None:
            tMax = self.t[-1]
        self.tMin=tMin
        self.tMax=tMax
        i=0
        while i<len(self.t) and self.t[i]<tMin:
            i+=1
        self.indicetMin=i     
        i=len(self.t)-1
        while i>0 and self.t[i]>tMax:
            i-=1
        self.indicetMax=i
     
    F = 96485.3329
    
    def meanlog (self, liste):
        summ=m.fsum(liste)
        mean = summ/(len(liste))
        return (mean)
    
    def linregress (self):
        moyt = self.meanlog (liste_transformation_log(self.t))
        moyI = self.meanlog (liste_transformation_log(self.I))
        #linearcoefficient=coefficient devant ln(t)
        #intercept=ln(nFCS*sqrt(D/pi))
        linearcoefficient = (m.fsum((m.log(t)-moyt)*(m.log(I)-moyI) for t,I in zip(self.t,self.I))/(m.fsum((m.log(t)-moyt)**2 for t in self.t))) 
        intercept = moyI-linearcoefficient*moyt
        return(linearcoefficient,intercept)
        
    def calculate_D (self, intercept, n, C, S):
        expintercept = m.exp (intercept)
        D = (expintercept**2*m.pi)/(n**2*self.F**2*S**2*C**2)
        return (D)                 

    def regression(self, n, S, C):

        """Effectue la régression linéaire et renvoie les valeurs de D et le
        coefficient directeur de la droite.
 
       Paramètres
        ----------
        n : entier
            Nombre d'électrons échangés au cours de la réaction.
        S : réel
            Surface d'échange (en cm²).
        C : réel
            Concentration de l'espèce.    
        Retour
        ------
        D : réel
            Valeur de D.
        coeffdirecteur : réel
            Coefficient directeur de la droite.
        """
    
        linearcoefficient, intercept = self.linregress(self.t[self.indicetMin : self.indicetMax],self.I[self.indicetMin:self.indicetMax])

        D = self.calculate_D (intercept, self.n , self.C , self.S)   

        return D, linearcoefficient, intercept
