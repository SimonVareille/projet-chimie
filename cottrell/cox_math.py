# -*- coding: utf-8 -*-
"""Pour la compatibilité avec python2"""
from __future__ import division
from math import sqrt, erf

def cox_curve(D, t, x):
    """Crée les valeurs de la courbe Cox pour `t` et `D` donnés selon 
    l'équation :
    
    `Cox = erf( x ÷ (2 × √(D × t) )`
    
    Paramètres
    ----------
    D : float
        Valeur de `D` (cm²•s-1).
    t : float
        Valeur de `t` (s).
    x : list
        Liste de valeurs de `x` (en cm).
    Retour
    ------
        Renvoie la liste de valeurs prises par `Cox`.
    Renvoie arbitrairement la fonction nulle si `constant = 0`.
    """
    constant = 2*sqrt(D*t)
    if constant == 0 : 
        return [ (0) for pos in x ]
    return [ (erf(pos/constant)) for pos in x ]
