#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
from cgi import FieldStorage
from mario_kart_files import get_generations

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<title>MK8: "lukelog"</title>
</head>
'''

last_generation = get_generations(1)

print "{}<br />".format(last_generation['generation number'])

for colour, player, character, vehicle in zip(
    last_generation['game info']['team colours'],
    last_generation['game info']['players'],
    last_generation['game info']['characters'],
    last_generation['game info']['vehicles']
):
    print "{},{},{},{}<br />".format(colour, player, character, vehicle)
