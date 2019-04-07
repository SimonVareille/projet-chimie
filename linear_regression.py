# -*- coding: utf-8 -*-

import math as m

def list_transformation_log (values):
    loglist=list()

    for i in (1,len(values)-1):
        loglist.append(m.log(values[i]))

    return (loglist)

def mean (liste):

    summ=m.fsum(liste)
    mean = summ/(len(liste))
    return (mean)

class LinearRegression:
    """Cette classe permet d'effectuer la régression linéaire sur les valeurs 
    expérimentales.
    """

    def __init__(self, t, I):
        self.t=t
        self.I=I
#        self.tMin=t[0]
#        self.tMax=t[-1]
#        self.indicetMin=0
#        self.indicetMax=len(t)-1
        self.Dexp=0
        
        
#    def set_t_interval(self, tMin=None, tMax=None):
        """Sélectionne l'intervalle dans lequel on veut effectuer la régression
        linéaire, si différent des valeurs du tableau.

        Paramètres
        ----------
        tMin : float
            Valeur minimale de `t`. La valeur effectivement prise en compte est
            la plus proche valeur supèrieure ou égale à `tMin` présente dans le
            tableau `t`.
            Si `tMin` est None, `tMin` prend la plus petite valeur de `t`.
        tMax : float
            Valeur maximale de `t`. La valeur effectivement prise en compte est
            la plus proche valeur infèrieure ou égale à `tMax` présente dans le
            tableau `t`.
            Si `tMax` est None, `tMax` prend la plus grande valeur de `t`.
        """

#        if tMin == None:
#            tMin = self.t[0]
#        if tMax == None:
#            tMax = self.t[-1]
#        self.tMin=tMin
#        self.tMax=tMax
#        i=0
#        while i<len(self.t) and self.t[i]<tMin:
#            i+=1
#        self.indicetMin=i     
#        i=len(self.t)-1
#        while i>0 and self.t[i]>tMax:
#            i-=1
#        self.indicetMax=i
     
    F = 96485.3329
    def logexp_curves_tab(self, expt, expI):
        self.logexpt= list_transformation_log(expt)
        self.logexpI=list_transformation_log(expI)
    
    def linregress (self):
        meant = mean(list_transformation_log(self.t))
        meanI = mean(list_transformation_log(self.I))
        #linearcoefficient=coefficient devant ln(t)
        #intercept=ln(nFCS*sqrt(D/pi))
        linearcoefficient = m.fsum(((t)-meant)*((I)-meanI) for t,I in zip(self.logexpt,self.logexpI))/(m.fsum(((t)-meant)**2 for t in self.logexpt)) 
        intercept = meanI-linearcoefficient*meant
        return(linearcoefficient,intercept)
        
    def logexp_and_linear_curves_tab (self, expt, expI):
        self.logexpt= list_transformation_log(expt)
        self.logexpI=list_transformation_log(expI)
        
        linearcoefficient, intercept= self.linregress()
        self.linlogexpI=[]
        for i in range (len(self.logexpt)) :
            self.linlogexpI.append(linearcoefficient*self.logexpt[i]+intercept)


    
        return (self.logexpt, self.logexpI, self.linlogexpI)
        
    def calculate_D (self, intercept, n, S, C):
        """Calcule le coefficient de diffusion D à l'aide des valeurs `n`, `S`
        et `C`.
        
        Paramètres
        ----------
        intercept : float
            Ordonnée à l'origine
        n : int
            Nombre d'électrons échangés au cours de la réaction.
        S : float
            Surface d'échange.
        C : float
            Concentration de l'espèce.
        
        Retour
        ------
        D : float
            
        """
        exponentialintercept = m.exp (intercept)
        D = (exponentialintercept**2*m.pi)/(n**2*self.F**2*S**2*C**2)
        self.Dexp=D
        return (D)             
    
#est ce qu on peut supprimer la fonction regression?
    def regression(self, n, S, C):
        """Effectue la régression linéaire pour obtenir le coefficient de 
        diffusion, le coefficinet directeur de la droite obtenue et son
        ordonnée à l'origine.
        
        Paramètres
        ----------
        n : int
            Nombre d'électrons échangés au cours de la réaction.
        S : float
            Surface d'échange.
        C : float
            Concentration de l'espèce.    
        Retour
        ------
        `tuple(D, linearcoefficient, intercept)`
        
        D : float
            Coefficient de diffusion.
        linearcoefficient : float
            Coefficient directeur de la droite.
        intercept : réel
            Ordonnée à l'origine de la droite.
        """
    
        linearcoefficient, intercept = self.linregress()#self.t[self.indicetMin : self.indicetMax],self.I[self.indicetMin:self.indicetMax])

        D = self.calculate_D (intercept, n, S, C)   

        return D, linearcoefficient, intercept
