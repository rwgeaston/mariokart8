#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from cgi import FieldStorage

from html_tools import html_table, dropdown_box
from stats_links import stats_links

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<title>MK8: Select Players</title>
<style>
select, body, html, p, input, a, checkbox {
    font-family:sans-serif;
    font-size:20pt;
}
table, select, input {
    width:100%;
    height:100px;
    text-align:center;
    font-size:24pt;
}
</style>
</head>
'''

current_handicaps_file = open('players.txt')
current_handicaps = current_handicaps_file.readlines()

player_list = [listing.split(',')[0] for listing in current_handicaps]

print '<form name="settings" action="generate.cgi" method="get"><br />'

print '''<b><p>The following things are not yet unlocked and so will not be randomly selected:</p>
<p>Gold Tyres</p></b>'''

checkboxes = [[]]

for player in sorted(player_list):
    if len(checkboxes[-1]) == 5:
        checkboxes.append([])
    checkboxes[-1].append(
        '<input type="checkbox" name="players" value="{player}"'
        ' id="{player}"><label for="{player}">{player_caps}</label><br>'
        .format(player=player, player_caps=player.capitalize()))

print html_table(checkboxes)
print '''<input type="submit" value="Generate teams"></form>'''

print stats_links()

print '</body></html>'
