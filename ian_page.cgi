#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
from cgi import FieldStorage

from html_tools import html_table, bold, paragraph
from mario_kart_files import get_generations

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<script src="sorttable.js"></script>
<title>MK8: Show result stats</title>
</head>
'''

if 'display_count' in GET:
    if GET['display_count'].value == 'all':
        display_count = -1
    else:
        try:
            display_count = int(GET['display_count'].value)
        except ValueError:
            display_count = 100
else:
    display_count = 100

generations = get_generations(display_count)

players = {}

for generation in generations:

    for player, colour in zip(
        generation['game info']['players'],
        generation['game info']['team colours']
    ):
        if player not in players:
            players[player] = {
                'paired with': {},
                'against': {},
            }

        for player2, colour2 in zip(
            generation['game info']['players'],
            generation['game info']['team colours']
        ):
            if player2 == player:
                continue

            if player2 not in players[player]['paired with']:
                players[player]['paired with'][player2] = 0
                players[player]['against'][player2] = 0

            if colour == colour2:
                players[player]['paired with'][player2] += 1
            else:
                players[player]['against'][player2] += 1

player_list = players.keys()
player_list.sort()

for direction in ['paired with', 'against']:
    table = [['-'] + player_list]
    for player in player_list:
        pairings_this_player = [player]
        for player2 in player_list:
            if player2 == player:
                pairings_this_player.append('-')
            elif player2 not in players[player][direction]:
                pairings_this_player.append(0)
            else:
                pairings_this_player.append(players[player][direction][player2])
        table.append(pairings_this_player)

    print bold(paragraph(direction))
    print html_table(table)

table = [['-'] + player_list]
for player in player_list:
    pairings_this_player = [player]
    for player2 in player_list:
        if player2 == player:
            pairings_this_player.append('-')
        elif player2 not in players[player][direction]:
            pairings_this_player.append('-')
        else:
            pairings_this_player.append(
                players[player]['paired with'][player2] * 100/
                (players[player]['paired with'][player2] + players[player]['against'][player2])
            )
    table.append(pairings_this_player)

print bold(paragraph("percentage of games both played on which they're on the same team (should be 33)"))
print html_table(table)
