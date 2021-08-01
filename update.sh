#!/usr/bin/sh

# update stats sheet with this week games
python Updater.py

# push new change to github
echo "\nPushing changes onto github ...\n"
git add Data/*
date=$(date '+%Y-%m-%d')
git commit -m "Weekly Update ($date)"
git push

