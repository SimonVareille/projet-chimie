# -*- coding: utf-8 -*-
from backports import csv
import os

class _DataRow:
    def __init__(self):
        self.name = ""
        self.values = []

class DataReader:
    """Classe s'occupant de lire un fichier affin d'obtenir les valeurs
    expérimentales.
    """
    def __init__(self, filename, delimiter = ';', encoding="ISO-8859-15"):
        """
        Initialisation de la classe.
        
        Paramètres
        ----------
        filename : str
            Nom du fichier csv ou crv à lire.
        delimiter : str
            Caractère délimitant les cellules (pour un fichier csv).
        encoding : str
            Type d'encodage du fichier.
        """
        self.tData = _DataRow()
        self.IData = _DataRow()
        
        if os.path.splitext(filename)[1] in (".csv", ".CSV"):
            self._csv_reader(filename)
        elif os.path.splitext(filename)[1] in (".crv", ".CRV"):
            self._crv_reader(filename)
        
    def _csv_reader(self, filename):
        leave = False
        for encoding in ("UTF-8", "ISO-8859-15"):
            if leave: break
            for delimiter in (',', ';'):
                try:
                    with open(filename, newline='', encoding=encoding) as csvfile:
                        self.rawData = csv.reader(csvfile, delimiter=delimiter)
                        data = list(self.rawData)
                        self.tData.name = data[0][0]
                        self.IData.name = data[0][1]
                        data = data[1:]
                        for row in data:
                            self.tData.values.append(float(row[0]))
                            self.IData.values.append(float(row[1]))
                except (OSError, ValueError):
                    break
                else:
                    leave = True
                    break
        if not leave:
            raise OSError()
            
    def _crv_reader(self, filename):
        leave = False
        for encoding in ("UTF-8", "ISO-8859-15"):
            try:
                with open(filename, newline='', encoding=encoding) as file:
                    for i in range(8):
                        file.readline()
                    lineNb = int(file.readline().rstrip('\n\r'))
                    for i in range(lineNb):
                        line = file.readline().rstrip('\n\r').split("\t")
                        self.tData.values.append(float(line[0]))
                        self.IData.values.append(float(line[1]))
            except FileNotFoundError as err:
                raise err
            except (OSError, ValueError) as err:
                pass
            else:
                leave = True
        if not leave:
            raise OSError()
    
    def get_t(self):
        """
        Retour
        ------
        Tableau de valeurs de t.
        """
        return self.tData.values
    
    def get_t_label(self):
        return self.tData.name
    
    def get_I(self):
        """
        Retour
        ------
        Tableau de valeurs de I.
        """
        return self.IData.values
    
    def get_I_label(self):
        return self.IData.name

    