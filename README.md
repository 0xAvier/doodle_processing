## Génération de fichier config

Génerer un fichier de config 'output' à partir du sondage de jeux :
`./main.py --generate_config_from_poll <date_poll_result>`


## Génération du fichier des possibilités
Ensuite, 
`./main.py -c output -s <date_poll_file> > o.csv`


## Génération des ics & stats 
./main.py -c output -s <processed_file> -i


## Options
### In [options] block
`nhosts` : le nombre de joueurs automatiquement ajouté à la table

`mandatory_player` : 

### On Games
Fief=5-6; early; owner=Xavier  
`early` : doit démarrer à 19h à la place de 19h30  
`owner` : propriétaire du jeu, doit être présent
