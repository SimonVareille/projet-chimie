from scipy.stats import linregress 
import numpy as np

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
        F = 96485.3329
        coeffdirecteur,_,_,_,_=linregress(1/(
                np.sqrt(self.t[self.indicetMin : self.indicetMax])),
                self.I[self.indicetMin:self.indicetMax])
        D = (coeffdirecteur**2 * np.pi)/(n**2 * F**2 * S**2 * C**2)    
        return D, coeffdirecteur
        

