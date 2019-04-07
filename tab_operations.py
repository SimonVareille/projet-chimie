# -*- coding: utf-8 -*-


class TabOperations():
    """Cette classe à pour objectif de faire des opérations sur le tableau des valeurs expérimentales    
    """
#    def __init__(self, tmin=None, tmax = None, expt= None, expI = None):
#        self.tmin = None
#        self.tmax = None
#        self.expt = None
#        self.expI = None    
#    def test_are_all_the_val_ok(self):
#        if (self.expt and self.expI and self.tmin!=None and self.tmax!=None):
#            self.are_all_the_val_ok = 1
#        else: 
#            self.are_all_the_val_ok=0 
        
    
    def rank_first_tmin(self, expt, tmin):
        """permet de savoir jusqu'à quel indice du tableau de expt et expI on va supprimer les valeurs"""
        value_to_return = 0
        while (value_to_return<len(expt) and expt[value_to_return] < tmin):
            value_to_return +=1
        return value_to_return
        
    def rank_last_tmax(self, expt, tmax):
        """permet de savoir à partir de quel indice du tableau de expt et expI on va supprimer les valeurs"""
        value_to_return = 0
        while (value_to_return<len(expt) and expt[value_to_return] < tmax):
            value_to_return +=1
        return value_to_return
    
    def del_values_not_between_tmin_tmax(self, expt, expI, tmin, tmax) :           
        """Cette fonction a pour objectif de supprimer les valeurs qui ne sont pas entre tmin et tmax
        dans le tableau des valeurs expérimentales    
        """
        tab_expt_to_return=[]
        tab_expI_to_return=[]
        rank_first=self.rank_first_tmin(expt,tmin)
        rank_last=self.rank_last_tmax(expt,tmax)
        for i in range(rank_first,rank_last):
            tab_expt_to_return.append(expt[i]-expt[rank_first]) #On commence à t=0
            tab_expI_to_return.append(expI[i])
        return tab_expt_to_return, tab_expI_to_return
        
        
        
        
        
        
        
        
        
        
        
        
        
