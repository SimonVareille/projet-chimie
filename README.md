# ReDoxLab
Application pour Android de visualisation de courbes de Cottrell


------
## Prérequis
Afin de pouvoir exécuter ce projet, il faut avoir installé les modules suivants: 
- `backports.csv` :  
    `pip install backports.csv` or  
    `conda install -c conda-forge backports.csv`
- `kivy` :  
    [](https://kivy.org/#download)
- `kivy-garden` :  
    [](https://kivy.org/doc/stable/api-kivy.garden.html)
- `kivy.garden.graph` :  
    [](https://kivy.org/doc/stable/api-kivy.garden.html)
- `KivyMD` :  
	[](https://github.com/HeaTTheatR/KivyMD)

------ 
## Compilation pour Android

:warning: **La compilation pour Android présentée ici sera probablement dépassée dans quelques années ! Buildozer est un outil en développement évoluant rapidement, des changements sont donc à prévoir !**  
Pour avoir des instructions à jour, consultez la [page GitHub de buildozer](https://github.com/kivy/buildozer). 

1. Installation de buildozer
    La première étape consiste à installer buildozer. Cet outil n'est disponible que sous Linux et l'installation se fait en ligne de commande . 
    Ce qui suit provient directement du *readme*.  
    
        # via pip (latest stable, recommended)
        sudo pip install buildozer
        
        # latest dev version
        sudo pip install   https://github.com/kivy/buildozer/archive/master.zip
    J'ai personnelement utilisé la deuxième méthode (installation depuis GitHub) car j'ai eu besoin d'un correctif n'ayant pas été déployé sur les serveurs Pypi.  

2. Configuration du projet (si non configuré)
    Pour configurer buildozer pour le projet en cours, allez dans le dossier de votre application et lancez :

        buildozer init
    Cela créera un fichier nommé `buildozer.spec` que vous devrez modifier pour donner le nom de votre application, son package, les dépendances...

3. Compilation
    Pour compiler, lancez :

        buildozer android debug
    Cela téléchargera les dépendances (python-for-android, android-sdk, android-ndk, apache-ant...). Ces composants sont volumineux, prévoyez donc du temps et une bonne connexion Internet.  
    Normalement, tout devrait s'installer automatiquement. Si vous rencontrez des erreurs, ouvrez `buildozer.spec` et changez `log_level` à `2`. Cela affichera plus d'informations lors de la compilation.  
    Si les problèmes proviennent de bibliothèques non installées ou non compatibles, suivez les instructions de la [page Read the Docs de buildozer](https://buildozer.readthedocs.io/en/latest/installation.html).
4. Transfert du `.apk` sur Android
    La compilation a créée un fichier nommé `<nom>-<version>-debug.apk` dans le dossier `bin` à la racine du projet. Pour l'envoyer sur un terminal Android connecté par usb, lancez :
    
        buildozer android deploy run

    Pour observer les messages de débogage générés par l'appli, décommentez la ligne `android.logcat_filters = *:S python:D` dans le fichier `buildozer.specs` et déployez l'appli avec :
    
        buildozer android deploy run logcat
