# too-tanky

## Introduction

too-tanky is an extensive, highly customizable League of Legends damage simulator. 
It can simulate the damage output between any combination of characters, level, items, runes etc...

It can also be extended to Teamfight Tactics in the future. 


## comment cloner le projet github dans windows

- Generate ssh key. Instruction [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=windows)
- Ouvrir le terminal, `cd` dans le dossier .ssh 
- faire `dir`
- La commande windows pour lire la clé publique ssh est `more id_qqchose.pub` 
- Copier la clé, coller dans les settings ssh github.

- Se placer à l'endroit ou on veut mettre le dossier.
- Pour cloner le repo, `git clone git@github.com:PaulQbFeng/too-tanky.git`

- Aller dans le dossier `too-tanky`, et faire `git status`

## Installer les dépendances

```
pip install -r requirements.txt -r requirements-dev.txt
```

## Formater

Pour garder un style uniforme, on formate le code avec [`isort`](https://pypi.org/project/isort/) et [`black`](https://pypi.org/project/black/).
Ceci peut être fait automatiquement avant chaque commit, avec la commande suivante qui crée un pre-commit hook avec le script `pre-commit.sh`:

```
ln -s ../../pre-commit.sh .git/hooks/pre-commit
```

On peut aussi simplement appliquer `isort` et `black` manuellement avant chaque `git add`, avec les commandes suivantes:

```
isort .
black .
```

## Tester

```
pytest
```
