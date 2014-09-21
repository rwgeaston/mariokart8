#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from json import dumps
import cgitb
from cgi import FieldStorage

from html_tools import html_table
from mario_kart_files import get_current_handicaps, get_generations_with_results

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

all_current_handicaps = get_current_handicaps()
everyone_ever_played = set()

generations = get_generations_with_results()
for generation in generations:
    if 'red score' in generations:
        everyone_ever_played.update(generation['game info']['players'])

if 'sort' in GET:
    if GET['sort'].value == 'alphabetical':
        all_current_handicaps.sort()
    elif GET['sort'].value == 'best':
        pass  # Text file should be written in this order anyway.
    elif GET['sort'].value == 'worst':
        all_current_handicaps.reverse()

handicaps = [["Player", "Handicap"]]

for player, handicap in all_current_handicaps:
    if player in everyone_ever_played:
        handicaps.append([player.capitalize(), handicap])

if 'machine_readable' in GET:
    print dumps(handicaps)
else:
    print html_table(handicaps)
