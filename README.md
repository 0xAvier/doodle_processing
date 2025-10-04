## Configuration des jeux

Génerer un fichier de configration pour les jeux à partir du sondage jeux:
`./main.py --generate_config_from_poll jeux.csv -o games.ini` 

Si vous utilisez un fichier de configuration globale pour les jeux, supprimer les sections `[games]` et `[options]` de `games.ini`.

## Génération du fichier des possibilités
Ensuite, 
`./main.py -c games.ini -s dates.csv > all.csv`

Le fichier de configuration fourni avec l'option -c  peut contenir les joueurs & jeux seulement les joueurs. 
Dans ce cas, les informations concernant les jeux doivent être fournies dans le fichier de configuration de jeux via l'option -g.
Dans ce cas, les [options] doivent s'y trouver. Se rapporter aux fichiers de tests pour des exemples.

`./main.py -c games.ini -s dates.csv -g all-games.ini > all.csv`

## Génération des ics & stats 
`./main.py -c games.ini -s selection.csv -i`

Ici, -g doit être passé également si il a été passé à l'étape précédente
`./main.py -c games.ini -s selection.csv -i -g all-games.ini`

## Options
### In [options] block
`nhosts` : le nombre de joueurs automatiquement ajouté à la table

`mandatory_player` : joueur qui doit être présent à la table pour que le jeu se lance

### On Games
Fief=5-6; early; owner=Xavier  
`early` : doit démarrer à 19h à la place de 19h30  
`owner` : propriétaire du jeu, doit être présent
