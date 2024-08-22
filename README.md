# Application de pilotage d'analyseur de spectre Anritsu

Le but de cette application est de piloter à distance (par wonnexion WiFi ou Ethernet) les analyseurs de spectres Anritsu via des commandes Telnet. Pour ce faire, nous allons utiliser la bibliothèque python Telnetlib qui nous permet d'envoyer de telle requêtes. Le résultat final sera une application dôtée d'une interface graphique générée grâce aux bibliothèques tkinter et matplotlib pour les graphes.

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