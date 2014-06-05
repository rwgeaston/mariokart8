#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from html_tools import html_table, dropdown_box
from cgi import FieldStorage
from random import randint, choice
import vehicle_data

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

def generation_error(message):
    print message.replace('\n', '<br />')
    print '<br /><a href="setup.cgi">Return to player selection.</a>'
    return

def main():
    for key in ['1', '2', '3', '4', 'force']:
        if key not in GET:
            return generation_error(
                'How did you get to this page?\n'
                'You don\'t have the correct GET keys.'
            )

    with open('players.txt') as current_handicaps_file:
        current_handicaps_raw = current_handicaps_file.readlines()

    current_handicaps = dict([listing.strip().split(',') for listing in current_handicaps_raw])
    player_list = [GET[str(player_number)].value for player_number in range(1, 5)]

    # error checking in the GET; probably needed because ob is allowed to use this site
    for player in current_handicaps:
        if player_list.count(player) > 1:
            if player != 'computer':
                return generation_error("The same person can't play twice.")

    for player in player_list:
        if player not in current_handicaps:
            return generation_error(
                "{} is not in the handicap system."
                .format(player.capitalize())
            )

    if 'computer' in player_list:
        found_computer = False
        for player in range(4):
            if found_computer:
                if player_list[player] != 'computer':
                    return generation_error("AI players must be bottom right first.")
            elif player_list[player] == 'computer':
                found_computer = True

    selections = {
        'players': player_list,
        'team selection': GET['force'].value,
        'handicaps before this game': [float(current_handicaps[player]) for player in player_list]
    }

    # team colour selection
    selections['team colours'] = [choice(['red', 'blue'])]
    if GET['force'].value == 'random':
        player_1_paired_with = randint(2, 4)
    else:
        player_1_paired_with = int(GET['force'].value)

    for player in range(2, 5):
        if player_1_paired_with == player:
            selections['team colours'].append(selections['team colours'][0])
        elif selections['team colours'][0] == 'red':
            selections['team colours'].append('blue')
        else:
            selections['team colours'].append('red')

    selections['characters'] = [choice(vehicle_data.characters.keys()) for i in range(4)]
    selections['vehicles'] = [choice(vehicle_data.vehicles.keys()) for i in range(4)]
    selections['tyres'] = [choice(vehicle_data.tyres.keys()) for i in range(4)]
    selections['gliders'] = [choice(vehicle_data.gliders.keys()) for i in range(4)]

    with open('generation_log.txt') as generation_log:
        try:
            last_gen_line = generation_log.readlines()[-1]
        except IndexError:
            # wow, first ever game
            generation_number = 1
        else:
            generation_number = int(last_gen_line.split(',')[0]) + 1

    with open('generation_log.txt', 'a') as generation_log:
        generation_log.write('{},{}\n'.format(generation_number, selections))

    print '''
<html>
<head>
<title>Show random team generation</title>
<meta http-equiv="refresh" content="1;url=show_game.cgi?gen={gen_num}">
    <script type="text/javascript">
        window.location.href = "show_game.cgi?gen={gen_num}"
    </script>
    <title>Page Redirection</title>
</head>
<body>
    If you are not redirected automatically, please click to see
    <a href="show_game.cgi?gen={gen_num}"> generation log</a>
</body>'''.format(gen_num=generation_number)
    return

main()
