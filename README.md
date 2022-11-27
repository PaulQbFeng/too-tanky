# too-tanky

## Introduction

too-tanky is an extensive, highly customizable League of Legends damage simulator. 
It can simulate the damage output between any combination of characters, level, items, runes etc...

It can also be extended to Teamfight Tactics in the future. 

## Project setup

Choose a directory to clone the project and `git clone git@github.com:PaulQbFeng/too-tanky.git`

### Environment setup  (Optional, ignore this if this is too complicated to setup)

Create environment `conda create -n myenv python=3.9` and activate it with `conda activate myenv`

### Install packages required for the project 

`pip install -r requirements.txt requirements-dev.txt`

Run `pytest` inside the working directory to test the setup.

## Workflow 

1. Ensure the `main` branch is up to date with `git pull origin main`. ---> `pytest` to check if all good
2. Create a branch from main to work on you feature `git checkout -b [branch-name]` + work on your feature
3. Write a test for your new feature and run `pytest` to check if your changes did not break anything
4. `git add [files modified]` / `git commit -m [message]` your changes
5. `git push origin [branch-name]` to create or update your branch in remote. 
6. Create a pull request from your branch into main and request a review from the other members .
7. If the pull request is approved, it can be merged inside main. 

... and go back to step 1 to develop a new feature !


## Dive in to the maths

- To understand champion base stat evolution per level: https://leagueoflegends.fandom.com/wiki/Champion_statistic
- To understand all the basics regarding damage calculation: https://docs.google.com/document/d/1wPY_ct0J45I3wxpHZgoLFAQKTSU2UfqF/edit?usp=sharing&ouid=100966089533647159501&rtpof=true&sd=true
- Details about runes (including adaptive runes): https://leagueoflegends.fandom.com/wiki/Rune_(League_of_Legends)
