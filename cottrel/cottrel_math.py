# -*- coding: utf-8 -*-

import math 

F = 96485.3329 #constante de Faraday en C.mol-1

def linspace(start, stop, num):
    '''Adaptée de `numpy.linspace`
    Crée un tableau commençant à `start`, finissant à `stop` contenant `num`
    éléments espacés régulièrement.
    
    Paramètres
    ----------
    start : float
        Valeur de départ de la séquence.
    stop : float
        Valeur de fin de la séquence.
    num : int
        Nombre d'éléments à générer
    
    Retour
    ------
    y : list
        `num` éléments régulièrement espacés dans l'intervalle fermé 
        `[start, stop]`
    '''
    if num < 0:
        raise ValueError("Number of samples, %s, must be non-negative." % num)
    div = num - 1

    delta = stop - start
    y = list(range(num))

    if num > 1:
        step = delta / div
        if step == 0:
            # Special handling for denormal numbers, gh-5437
            y = [i/div*delta for i in y]
        else:
            y = [i*step for i in y]
    else:
        y = [i*delta for i in y]

    y = [i+start for i in y]

    if num > 1:
        y[-1] = stop
   
    return y

def create_t(start, stop, num):
    '''Crée un tableau commençant à `start`, finissant à `stop` contenant `num`
    éléments espacés régulièrement. Si `start == 0` la première valeur est
    éliminée, le tableau possède alors `num-1` éléments.
    
    Paramètres
    ----------
    start : float
        Valeur de départ de la séquence.
    stop : float
        Valeur de fin de la séquence.
    num : int
        Nombre d'éléments à générer
    
    Retour
    ------
     : list
        `num` éléments régulièrement espacés dans l'intervalle fermé 
        `[start, stop]` si `start != 0`.
    '''
    if start==0:
        return linspace(start, stop, num)[1:]
    return linspace(start, stop, num)

def cottrel_curve_gen(n, S, C, D, t):
    '''Crée un tableau de valeurs d'intensité selon l'équation de Cottrel : 
        `I = n × F × S × C × √(D ÷ (π × t))`

        Paramètres
        ----------
        n : int
            Nombre d'électrons échangés au cours de la réaction. (mol)
        S : float
            Surface d'échange de l'électrode. (cm²)
        C : float
            Concentration interfaciale de l'espèce chimique étudiée. (mol•cm-3)
        D : float
            Coefficient de diffusion de l'espèce chimique étudiée. (cm²•s-1)
        t : list-like
            Valeurs de t pour lesquelles on veut calculer l'intensité. (s)
        
        Retour
        ------
        I : list
            Valeurs de l'intensité pour les temps `t`. (A)
    '''
    constant = n*F*S*C*math.sqrt(D/math.pi)
    
    return[ (constant*math.sqrt(1/time)) for time in t ]
