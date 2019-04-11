# -*- coding: utf-8 -*-

class TabOperations():
    """Cette classe a pour objectif de faire des opérations sur les tableaux des 
    valeurs expérimentales.
    """
        
    
    def rank_first_t(expt, t):
        """Permet de savoir jusqu'à quel indice du tableau de `expt` et `expI` 
        on va supprimer les valeurs.
        
        Paramètres
        ----------
        expt : list
            Tableau de valeurs ordonné à analyser.
        t : float
            Valeur à chercher.
        
        Retour
        ------
        Retourne l'indice de la première valeur de `expt` supérieure ou égale
        à `t`.
        Retourne `len(expt)` si l'indice n'est pas trouvé.
        """
        value_to_return = 0
        while (value_to_return < len(expt) and expt[value_to_return] < t):
            value_to_return +=1
        return value_to_return
    
    def del_values_not_between_tmin_tmax(expt, expI, tmin, tmax) :           
        """Cette fonction a pour objectif de supprimer les valeurs qui ne sont 
        pas entre `tmin` et `tmax` dans le tableau des valeurs expérimentales.
        """
        tab_expt_to_return=[]
        tab_expI_to_return=[]
        
        rank_first = TabOperations.rank_first_t(expt,tmin)
        rank_last = TabOperations.rank_first_t(expt,tmax)

        for i in range(rank_first,rank_last):
            tab_expt_to_return.append(expt[i]-expt[rank_first]) #On commence à t=0
            
        tab_expI_to_return = expI[rank_first : rank_last]
        return tab_expt_to_return, tab_expI_to_return
    
    def add_x_to_tab(tab, x):
        """Permet d'ajouter une valeur à toutes les valeurs d'un tableau.
        
        Paramètres
        ----------
        tab : list
            Tableau de valeurs à modifié.
        x : float
            Valeur à ajouter.
        
        Retour
        ------
        Retourne le tableau modifié.
        """
        tab_to_return=[]
        for i in range (len(tab)):
            tab_to_return.append(tab[i]+x)
        return tab_to_return
        
        
        
        
        
        
        
        
        
        
        
        
