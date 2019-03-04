# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
from backports import csv

class _DataRow:
    def __init__(self):
        self.name = ""
        self.values = []

class DataReader():
    """Classe s'occupant de lire un fichier CSV affin d'obtenir les valeurs
    expérimentales.
    """
    def __init__(self, filename, delimiter = ";", encoding='ISO-8859-15'):
        """
        Paramètres
        ----------
        filename : str
            Nom du fichier csv à lire.
        delimiter : str
            Caractère délimitant les cellules.
        """
        self.tData = _DataRow()
        self.IData = _DataRow()
        
        with  io.open(filename, newline='', encoding=encoding) as csvfile:
            self.rawData = csv.reader(csvfile, delimiter=delimiter)
            data = list(self.rawData)
            self.tData.name = data[0][0]
            self.IData.name = data[0][1]
            data = data[1:]
            for row in data:
                self.tData.values.append(float(row[0]))
                self.IData.values.append(float(row[1]))
                
    def get_t(self):
        return self.tData.values
    
    def get_t_label(self):
        return self.tData.name
    
    def get_I(self):
        return self.IData.values
    
    def get_I_label(self):
        return self.IData.name
            