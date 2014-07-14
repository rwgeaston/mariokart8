#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from html_tools import html_table
from cgi import FieldStorage
from json import dumps

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

current_handicaps_file = open('players.txt')
current_handicaps = current_handicaps_file.readlines()

everyone_ever_played = set()

with open('results_log.txt') as results_log:
    for line in results_log.readlines():
        players_this_result = eval(line)[2]
        everyone_ever_played.update(set(players_this_result))

if 'sort' in GET:
    if GET['sort'].value == 'alphabetical':
        current_handicaps.sort()
    elif GET['sort'].value == 'best':
        pass # text file should be written in this order anyway
    elif GET['sort'].value == 'worst':
        current_handicaps.reverse()

handicaps = [["Player", "Handicap"]]

for line in current_handicaps:
    player, handicap = line.strip().split(',')
    if player in everyone_ever_played:
        handicaps.append([player.capitalize(), handicap])

if 'machine_readable' in GET:
    print dumps(handicaps)
else:
    print html_table(handicaps)
