#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from html_tools import html_table
from cgi import FieldStorage
import vehicle_data

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<title>MK8: Show Random Team Generation</title>
<style>
.red_team {
    color: red;
}

.blue_team {
    color: blue;
}
</style>
</head>
'''

def show_selection(player_number):


def main():
    if 'gen' not in GET:
        print "You don't have a gen value in the GET. How did you get to this page?"
        return

    with open('generation_log.txt') as generation_log:
        for generation in generation_log.readlines():
            gen_number, selection = eval(generation)
            if str(gen_number) == GET['gen'].value:
                break
        else:
            print "I can't find that generation number. How did you get to this page?"
            return
    print "<p class='red_team'>"
    print selection
    print "</p>"
    return

    print html_table([
        [show_selection(selection, 1), show_selection(selection, 2)],
        [show_selection(selection, 3), show_selection(selection, 4)]
    ])

main()