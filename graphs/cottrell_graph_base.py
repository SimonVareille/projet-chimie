# -*- coding: utf-8 -*-

class CottrellGraphBase:
    """Classe mère permettant d'avoir une base commune pour
    la création du graphique principal, quelque soit l'interface graphique 
    utilisée.
    """
    def __init__(self, t=[], I=[]):
        self.t=t
        self.I=I
        self.n=1
        self.S=1
        self.C=10**-3
        self.D=10**-5

        self.expt=[]
        self.expI=[]

        self.expD = None

        self._display_theoric=True
        self._display_experimental=False

        self.tleft=0
        self.tright = max(t) if t else 5
        self.Ibottom=0
        self.Itop = max(I) if I else 2
        
    def set_n (self, n):
        self.n=n
    def get_n(self):
        return self.n
        
    def set_S (self, S):
        self.S=S
    def get_S(self):
        return self.S   
             
    def set_C (self, C):
        self.C=C
    def get_C(self):
        return self.C
        
    def set_D (self, D):
        self.D=D
    def get_D(self):
        return self.D
    
    def display_theoric(self, displayTheoric = True):
        """Affiche la courbe théorique si `displayTheoric == True`.
        """
        self._display_theoric=displayTheoric
    
    def is_theoric_displayed(self):
        return self._display_theoric
        
    def set_theoric_data (self, t, I):
        self.t=t
        self.I=I
    def get_theoric_data(self):
        return self.t, self.I
        
    def display_experimental(self, displayExperimental = True):
        """Affiche la courbe expérimentale si `displayTheoric == True`.
        """
        self._display_experimental=displayExperimental
        
    def is_experimental_displayed(self):
        return self._display_experimental

    def set_experimental_data(self, expt, expI):
        self.expt=expt
        self.expI=expI
        
    def set_limit_interval(self, tleft=None, tright=None, Ibottom=None, Itop=None):
        """Sélectionne la zone que l'on veut afficher. Par défaut l'ensemble 
        des points est affiché.
        
        Paramètres
        ----------
        tleft : float
            Valeur minimale de l'abscisse.
        tright : float
            Valeur maximale de l'abscisse.
        Ibottom : float
            Valeur minimale de l'ordonnée.
        Itop : float
            Valeur maximale de l'ordonnée.
        
        `Ǹone` initialise le paramètre automatiquement pour contenir l'ensemble
        des données.
        """
        if tleft == None:
            tleft = 0
        if tright == None:
            if self._display_theoric:
                tright = max(self.expt) if self._display_experimental else max(self.t)
            else:
                tright = max(self.expt) if self._display_experimental else 5
        if Ibottom == None:
            Ibottom = 0
        if Itop == None:
            if self._display_theoric:
                Itop = max(self.expI) if self._display_experimental else max(self.I)
            else:
                Itop = max(self.expI) if self._display_experimental else 1
        
        self.tleft=tleft
        self.tright=tright
        self.Ibottom=Ibottom
        self.Itop=Itop
