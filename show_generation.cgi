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

def show_selection(selection, player_number):
    return '''
<p class='{team_colour}_team'>
{character}<br />
{vehicle}<br />
{tyres}<br />
{glider}<br /></p>'''.format(
        team_colour=selection['team colours'][player_number],
        character=selection['characters'][player_number],
        vehicle=selection['vehicles'][player_number],
        tyres=selection['tyres'][player_number],
        glider=selection['gliders'][player_number]
    )

def selection_stats(selection, player_number):
    weight_class = vehicle_data.characters[selection['characters'][player_number]]
    player_stats = vehicle_data.character_classes[weight_class]
    vehicle_stats = vehicle_data.vehicles[selection['vehicles'][player_number]]
    tyre_stats = vehicle_data.tyres[selection['tyres'][player_number]]
    glider_stats = vehicle_data.gliders[selection['gliders'][player_number]]
    overall_stats = map(sum, zip(player_stats, vehicle_stats, tyre_stats, glider_stats))
    overall_stats_strings = [str(element) for element in overall_stats]
    return ["<p class='{team_colour}_team'>{player_name}</p>"
            .format(
                team_colour=selection['team colours'][player_number],
                player_name=selection['players'][player_number]),
            str(selection['handicaps before this game'][player_number])] + \
            overall_stats_strings

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

    print html_table([
        [show_selection(selection, 0), show_selection(selection, 1)],
        [show_selection(selection, 2), show_selection(selection, 3)]
    ])

    print '<br />'

    print html_table(
        [['Player', 'Handicap', 'Speed', 'Accel', 'Weight', 'Handling', 'Grip']] +
        [selection_stats(selection, player_number) for player_number in range(4)]
    )

    net_red_handicap = 0
    for player_num in range(4):
        if selection['team colours'][player_num] == 'red':
            net_red_handicap += selection['handicaps before this game'][player_num]
        else:
            net_red_handicap -= selection['handicaps before this game'][player_num]

    red_to_win = int(205 + net_red_handicap / 2.0 + 1)
    blue_to_win = int(205 - net_red_handicap / 2.0 + 1)
    red_to_change = int(205 + net_red_handicap / 2.0 + 3)
    blue_to_change = int(205 - net_red_handicap / 2.0 + 3)

    print ("<p class='red_team'>"
           "Red team needs {} to win and {} for handicap to change."
           "</p>"
          .format(red_to_win, red_to_change))

    print ("<p class='blue_team'>"
           "Blue team needs {} to win and {} for handicap to change."
           "</p>"
          .format(blue_to_win, blue_to_change))

    print '<form name="submit" action="submit.cgi" method="post">'
    print 'Red team final score: <input type="text" name="redscore"><br><br>'
    print '<input type="hidden" name="gen" value="{}" />'.format(GET['gen'].value)
    print '<input type="submit" value="Submit result"></form>'

    print '</html>'

    return

main()
