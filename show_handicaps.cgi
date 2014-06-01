#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from html_tools import html_table
from cgi import FieldStorage

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

current_handicaps_file = open('players.txt')
current_handicaps = current_handicaps_file.readlines()

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
	handicaps.append([player.capitalize(), handicap])

print html_table(handicaps)