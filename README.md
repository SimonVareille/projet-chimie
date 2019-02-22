# Projet-Chimie
Le repo du projet, le nom pourra être changé ulterieurement.

------
### Prérequis
Afin de pouvoir exécuter ce projet, il faut avoir installé les modules suivants:
- `numpy`, `scipy` et `matplotlib` :
    https://www.scipy.org/install.html
- `kivy` :
    https://kivy.org/#download
- `kivy-garden` :
    https://kivy.org/doc/stable/api-kivy.garden.html
- `kivy.garden.matplotlib` et `kivy.garden.graph`
    https://kivy.org/doc/stable/api-kivy.garden.html
    En remplaçant `graph` par `matplotlib` pour installer `kivy.garden.matplotlib`

------

On peut maintenant lancer `main.py`. Cela affiche la courbe principale mais ce n'est pas encore interractif.

Pour utiliser `kivy.garden.graph`, il suffit de changer la valeur de `USE_MATPLOTLIB` du fichier `config.py` à `False`.
Pour ne pas utiliser `numpy`, il suffit de changer la valeur de `USE_NUMPY` du fichier `config.py` à `False`.
      
