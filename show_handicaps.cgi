#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from json import dumps
import cgitb
from cgi import FieldStorage

from html_tools import html_table
from mario_kart_files import get_current_handicaps, get_generations_with_results
from decay import recent_players

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

all_current_handicaps = get_current_handicaps()

if 'sort' in GET:
    if GET['sort'].value == 'alphabetical':
        all_current_handicaps.sort()
    elif GET['sort'].value == 'best':
        pass  # Text file should be written in this order anyway.
    elif GET['sort'].value == 'worst':
        all_current_handicaps.reverse()

if 'display_count' in GET:
    if GET['display_count'].value == 'all':
        display_count = 10000
    else:
        try:
            display_count = int(GET['display_count'].value)
        except ValueError:
            display_count = 50
else:
    display_count = 50

handicaps = [["Player", "Handicap"]]
recent = recent_players(game_count=display_count)

for player, handicap in all_current_handicaps:
    if player in recent:
        handicaps.append([player, handicap])

if 'machine_readable' in GET:
    print dumps(handicaps)
else:
    print html_table(handicaps)
