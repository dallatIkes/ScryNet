# Application de pilotage d'analyseur de spectre Anritsu MS2090A FieldMaster Pro

Le but de cette application est de piloter à distance (par wonnexion WiFi ou Ethernet) les analyseurs de spectres Anritsu via des commandes Telnet. Pour ce faire, nous allons utiliser la bibliothèque python Telnetlib qui nous permet d'envoyer de telle requêtes. Le résultat final sera une application dôtée d'une interface graphique générée grâce aux bibliothèques tkinter et matplotlib pour les graphes.

Libre à vous de récupérer le projet et de le modifier pour satisfaire vos besoins ;)

## Guide d'installation

Premièrement, il va falloir récupérer le projet. Pour cela, deux options s'offrent à vous :

- **Utiliser le terminal**  
  Ouvrez [git bash](https://git-scm.com/downloads) et déplacez-vous dans le répoertoire de votre choix. Puis entrez la commande suivante
  ```bash
  git clone https://github.com/dallatIkes/ScryNet.git
  ```
  
- **Utiliser l'interface graphique**  
  Sur github, télécharger l'archive du projet et décompressez la dans le répoertoire de votre choix

  Une fois le projet téléchargé, il va falloir l'installer. Pour ce faire, ouvrez [git bash](https://git-scm.com/downloads) dans le répertoire du projet et tapez la commande suivante
  ```bash
  ./make.sh build
  ```
  L'installation va se lancer et après quelques secondes, vous trouverez le fichier exécutable dans le dossier dist. Pour plus de confort, n'hésitez pas à créer un raccourci bureau de ce fichier (sans le déplacer) 

## Guide d'utilisation

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
