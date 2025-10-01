## Génération de fichier config

Génerer un fichier de config 'output' à partir du sondage de jeux :
`./main.py --generate_config_from_poll jeux.csv -o output` 

L'argument -o est optionnel.


## Génération du fichier des possibilités
Ensuite, 
`./main.py -c output -s dates.csv > all.csv`

Le fichier de configuration pris en compte par défaut est 'config' mais peut-être remplacé en l'indiquant avec l'option -c 
Il peut contenir uniquement les joueurs & jeux seulement les joueurs. Dans ce cas, les informations concernant les jeux doivent être fournies dans le fichier de configuration de jeux via l'option -g.
Dans ce cas, les [options] doivent s'y trouver. Se rapporter aux fichiers de tests pour des exemples.

`./main.py -c output -s dates.csv -c config -g game_config > all.csv`


## Génération des ics & stats 
./main.py -c output -s selection.csv -i


## Options
### In [options] block
`nhosts` : le nombre de joueurs automatiquement ajouté à la table

`mandatory_player` : joueur qui doit être présent à la table pour que le jeu se lance

### On Games
Fief=5-6; early; owner=Xavier  
`early` : doit démarrer à 19h à la place de 19h30  
`owner` : propriétaire du jeu, doit être présent
