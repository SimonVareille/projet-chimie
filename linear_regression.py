# -*- coding: utf-8 -*-

import math as m

def list_transformation_log (values): 
    """Crée une liste du logarithme népérien de chaque valeur 
    d'une liste.
        
    Paramètres
    ----------
    values : list
        Tableau de valeurs

    Retour
    ------
    loglist : list
        Tableau de valeurs log

    """
    loglist=list()
    #on élimine la première valeur du tableau car elle 
    #correspond à t=0 dont on ne peut pas prendre le log
    for val in values[1:]: 
        loglist.append(m.log(val))
    return (loglist)

def mean (liste):
    """Calcule la moyenne d'une liste.
    """
    
    summ=m.fsum(liste)
    mean = summ/(len(liste))
    return (mean)

class LinearRegression:
    """Permet d'effectuer la régression linéaire sur les valeurs 
    expérimentales.
    """

    def __init__(self, t, I):
        """
        Paramètres
        ----------
        t : list
            Tableau de valeurs des temps expérimentaux.
        I : list
            Tableau de valeurs des intensités mesurées expérimentalement.
        """
        self.t=t
        self.I=I
        self.Dexp=0
        
    F = 96485.3329  #Constante de Faraday
    
    def logexp_curves_tab(self, expt, expI):
        """Calcule les listes des valeurs logarithmiques des 
        listes du temps et de l'intensité.
        
        Paramètres
        ----------
        expt : list
            Tableau de valeurs des temps expérimentaux.
        expI : list
             Tableau de valeurs des intensités expérimentales.
        
        """
        self.logexpt= list_transformation_log(expt)
        self.logexpI= list_transformation_log(expI)
    
    def linregress (self):
        """Calcule, à l'aide de formules mathématiques et 
        par le modèle des moindres carrés, le coefficient directeur et 
        l'ordonnée à l'origine de la droite de régression linéaire. 
        
        Retour
        ------
        linearcoefficient : float
            Coefficient directeur de la droite de régression linéaire.
        intercept : float
            Ordonnée à l'origine de la droite de régression linéaire.
        
        """
        meant = mean(list_transformation_log(self.t))
        meanI = mean(list_transformation_log(self.I))
        linearcoefficient = m.fsum( (t-meant)*(I-meanI) for t,I in zip(self.logexpt,self.logexpI) )\
            / ( m.fsum(((t)-meant)**2 for t in self.logexpt) ) 
        intercept = meanI-linearcoefficient*meant
        return(linearcoefficient,intercept)
        
    def logexp_and_linear_curves_tab (self, expt, expI):
        """Calcule la liste des valeurs de la droite de régression 
        linéaire.
        
        Paramètres
        ----------
        expt : list
            Tableau de valeurs des temps expérimentaux.
        expI : list
            Tableau de valeurs des intensités expérimentales.
            
        Retour
        ------
        linlogexpI : list
            Tableau des valeurs d'intensité de la droite de régression linéaire.
        """
        self.logexp_curves_tab (expt, expI)
        
        linearcoefficient, intercept= self.linregress()
        self.linlogexpI=[]
        for i in range (len(self.logexpt)) :
            self.linlogexpI.append(linearcoefficient*self.logexpt[i]+intercept)

        return (self.logexpt, self.logexpI, self.linlogexpI)
        
    def calculate_D (self, intercept, n, S, C):
        """Calcule le coefficient de diffusion D à l'aide des valeurs `n`, `S`
        , `C` et de l'ordonnée à l'origine .
        
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
            Coefficient de diffusion retrouvé expérimentalement
            
        """
        exponentialintercept = m.exp (intercept)
        D = (exponentialintercept**2*m.pi)/(n**2*self.F**2*S**2*C**2)
        self.Dexp=D
        return (D)             
       
        
