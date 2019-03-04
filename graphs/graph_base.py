# -*- coding: utf-8 -*-

class MainGraphBase:
    """Cette classe est la classe mère permettant d'avoir une base commune pour
    la création du graphique principal, que l'on utilise **matplotlib** ou 
    **kivy.garden.graph**.
    Les variables `n`, `S`, `C` et `D` ne sont peut-être pas utiles dans cette
    classe... À voir...
    """
    def __init__(self, t, I):
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
        self.tright=max(t)
        self.Ibottom=0
        self.Itop=max(I)
        
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
        self._display_theoric=displayTheoric
    
    def is_theoric_displayed(self):
        return self._display_theoric
        
    def set_theoric_data (self, t, I):
        self.t=t
        self.I=I
        #self.I=cottrel.courbe_cottrel_th(self.n, self.S, self.C, self.D, self.t)
    def get_theoric_data(self):
        return self.t, self.I
        
    def display_experimental(self, displayExperimental = True):
        self._display_experimental=displayExperimental
        
    def is_experimental_displayed(self):
        return self._display_experimental

    def set_experimental_data(self, expt, expI):
        self.expt=expt
        self.expI=expI
        
    def set_expD(self, expD) :
        self.expD=expD
        
    def set_limit_interval(self, tleft=None, tright=None, Ibottom=None, Itop=None):
        """Sélectionne la zone que l'on veut afficher. Par défaut l'ensemble 
        des points est affiché.
        """
        if tleft == None:
            tleft = 0
        if tright == None:
            tright = max(max(self.t), max(self.expt)) if self._display_experimental else max(self.t)
        if Ibottom == None:
            Ibottom = 0
        if Itop == None:
            Itop = max(max(self.I), max(self.expI)) if self._display_experimental else max(self.I)
        
        self.tleft=tleft
        self.tright=tright
        self.Ibottom=Ibottom
        self.Itop=Itop
