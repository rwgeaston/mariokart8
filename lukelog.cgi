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
<title>MK8: "lukelog"</title>
</head>
'''

with open("generation_log.txt") as generation_log_file:
    generations = generation_log_file.readlines()

last_gen_number, last_generation = eval(generations[-1])

print "{}<br />".format(last_gen_number)

for colour, player, character, vehicle in zip(
    last_generation['team colours'], 
    last_generation['players'],
    last_generation['characters'],
    last_generation['vehicles']
):
    print "{},{},{},{}<br />".format(colour, player, character, vehicle)
