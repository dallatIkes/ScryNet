# Application de pilotage d'analyseur de spectre Anritsu MS2090A FieldMaster Pro : ScryNet

Le but de ScryNet est de piloter à distance (par connexion WiFi ou Ethernet) les analyseurs de spectre Anritsu via des commandes Telnet. Pour ce faire, nous allons utiliser la bibliothèque python Telnetlib qui nous permet d'envoyer de telles requêtes. Le résultat final sera une application dotée d'une interface graphique générée grâce aux bibliothèques tkinter et matplotlib pour les graphes.

Libre à vous de récupérer le projet et de le modifier pour satisfaire vos besoins ;)

## Guide d'installation

Premièrement, il va falloir récupérer le projet. Pour cela, deux options s'offrent à vous :

- **Utiliser le terminal**  
  Ouvrez [git bash](https://git-scm.com/downloads) et déplacez-vous dans le répertoire  de votre choix. Puis entrez la commande suivante :
  ```bash
  git clone https://github.com/dallatIkes/ScryNet.git
  ```
  
- **Utiliser l'interface graphique**  
  Sur github, télécharger l'archive du projet et décompressez-la dans le répertoire  de votre choix.
  
[//]: # ()
      
  Une fois le projet téléchargé, il va falloir l'installer. Pour ce faire, ouvrez [git bash](https://git-scm.com/downloads) dans le répertoire du projet et tapez la commande suivante :
  ```bash
  ./make.sh build
  ```
  L'installation va se lancer et après quelques secondes, vous trouverez le fichier exécutable dans le dossier ``./dist/``. Pour plus de confort, n'hésitez pas à créer un raccourci bureau de ce fichier (sans le déplacer). 

## Guide d'utilisation

Pour l'instant, ScryNet dispose de 3 fenêtres principales :
- **Paramètres**  
  Fenêtre pour gérer le paramétrage général de l'instrument :
  - Fréquence limite à gauche en GHz (min = 0)
  - Fréquence limite à droite en GHz (max = 9)
  - Amplitude limite en haut en dB
  - Échelle d'amplitude en dB/div
  - Largeur de bande en Hz
    
  [//]: # ()
    
    **Note:** Les paramètres par défaut sont ceux récupérés par l'appareil. Pour les modifier, renseignez les paramètres voulus dans les champs correspondants et appuyez sur le bounton ``Appliquer`` ou utilisez la touche ``Entrée`` du clavier.

    Des presets sont également disponibles pour les paramètres récurrents:
    - WiFi2 : [2.4; 2.5] GHz
    - WiFi4 : [5.170; 5.730] GHz
    - WiFi6E : [5.925; 6.425] GHz
 
      [//]: # ()
      
      **Note:** 3 autres boutons de presets sont disponibles  référez vous au guide de programmation pour les personnaliser.
  
- **Traces**
  Fenêtre pour gérer les traces de l'instrument une par une :
  - Type : Clear/Write; Maximum; Minimum; Average
  - Mode : Active; Hold/View; Blank
    
- **Visualisation**
  Fenêtre pour visualiser les traces actives sur l'instrument. Une fois sur la fenêtre, la génération du graphe se lance automatiquement. Si jamais vous voulez rafraîchir le graphe, vous pouvez le faire à l'aide du raccourci clavier ``Ctrl+R``. Pour enregistrer le graphe affiché, appuyez sur ``Ctrl+S``. Une fenêtre s'ouvrira avec un nom de fichier par défaut (date d'enregistrement) que vous pouvez modifier. Après confirmation, vous trouverez l'image enregistrée dans le répertoire ``./saves/``.

## Guide de programmation

## Cahier des charges

- [x] param
```python
# définit les paramètres de visualisation de l'instrument
def param(fdeb, ffin, amplRef, amplCase, vit):
    # fdeb      : fréquence limite gauche
    # ffin      : fréquence limite droite
    # amplRef   : amplitude limite haut
    # amplCase  : dB/div
    # vit       : bandwidth
```
- [ ] autoVisu
```python
# renvoie les paramètres correspondant selon la bande à observer
def autoVisu(bande):
    # bande : ['2', '5', '6', 'large']
```
- [ ] amplAuto
```python
# trouve automatiquement les paramètres d'amplitude à sélectionner
def amplAuto():
```
- [x] trace
```python
# clear puis mesure selon le mode
def trace(num, mode, nbMesure):
    # num       : numéro de la trace
    # mode      : ['clear/write', 'min', 'max', 'average']
    # nbMesure  : nombre de mesures avant le hold (0 pour clear/write)
```
- [x] reset
```python
# supprime toutes les traces hold
def reset():
```
- [x] suppr
```python
# blank une trace
def suppr(num):
    # num   : numéro de la trace
```
- [ ] export
```python
# enregistre toutes les traces dans un fihcier excel
def export(name):
    # name  : nom du fichier
```
- [ ] wifi
```python
# affiche toutes les fréquences de début et fin du canal wifi
def wifi():
```
- [x] affich
```python
# affiche la courbe actuelle visible sur l'instrument
def affich():
```
