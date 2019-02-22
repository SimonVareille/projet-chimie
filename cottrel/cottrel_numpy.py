# -*- coding: utf-8 -*-
import numpy as np

F = 96485.3329

def create_t(start, stop, num):
    if start==0:
        return np.linspace(start, stop, num)[1:]
    return np.linspace(start, stop, num)

def courbe_cottrel_th(n, S, C, D, t):
    I = n*F*S*C*np.sqrt(D/np.pi)*np.sqrt(1/t)
    return I
