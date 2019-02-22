from math import sqrt, erfc

def cox_curve(D, t, x):
    """Crée les valeurs de la courbe Cox pour `t` et `D` donnés.
    Paramètres
    ----------
    D : réel
        Valeur de `D` ( != 0).
    t : réel
        Valeur de `t` ( != 0).
    x : list
        Liste de valeurs de `x` (en cm).
    Retour
    ------
        Renvoie la liste de valeurs prises par `Cox`
    """
    constant = 2*sqrt(D*t)
    return [ erfc(pos/constant) for pos in x ]