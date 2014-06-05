#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from html_tools import html_table, dropdown_box
from cgi import FieldStorage

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<title>MK8: Select Players</title>
</head>
'''

current_handicaps_file = open('players.txt')
current_handicaps = current_handicaps_file.readlines()

player_list = [listing.split(',')[0] for listing in current_handicaps]

def player_dropdown(position):
    return dropdown_box(
        str(position), 
        player_list, 
        'computer', 
        [player.capitalize() for player in player_list]
    )

player_generation_table = [
    [player_dropdown(1), player_dropdown(2)],
    [player_dropdown(3), player_dropdown(4)]]


print '<form name="settings" action="generate.cgi" method="get"><br />'

print html_table(player_generation_table)

print (
    '<br />Optional force team selection. '
    'Player 1 (top left) must be paired with:<br />{}<br /><br />'
    .format(
        dropdown_box('force',
        ['random', '2', '3', '4'],
        'random',
        ['Random',
         'Player 2 (top right)',
         'Player 3 (bottom left)',
         'Player 4 (bottom right)']
        )
    )
)

print '''
<input type="submit" value="Generate teams"></form>

<p><a href="show_handicaps.cgi">See current handicaps</a></p>
<p><a href="recent_games.cgi?display_count=10">See previously generated games</a></p>
<p><a href="recent_games.cgi?completed_only=true&display_count=10">
    See games with submitted results only</a></p>

</body></html>'''
