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

## Tester

- Installer pytest `pip install -r requirements-dev.txt`
- Lancer `pytest`
