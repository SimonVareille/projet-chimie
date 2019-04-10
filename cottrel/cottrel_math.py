# -*- coding: utf-8 -*-

from __future__ import division #Pour la compatibilité avec python2

import math 

F = 96485.3329 #constante de Faraday

def linspace(start, stop, num):
    '''Cette fonction est adaptée de  `numpy.linspace`
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
    if start==0:
        return linspace(start, stop, num)[1:]
    return linspace(start, stop, num)

def courbe_cottrel_th(n, S, C, D, t):
    constant = n*F*S*C*math.sqrt(D/math.pi)
    
    return[ (constant*math.sqrt(1/time)) for time in t ]
