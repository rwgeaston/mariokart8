#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
from cgi import FieldStorage
from random import randint, choice, shuffle

import vehicle_data
from mario_kart_files import get_current_handicaps, append_generation

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
    if isinstance(GET['players'], list):
        player_list = [player.value for player in GET['players']]
    else:
        player_list = [player for player in GET['players'].value]

    current_handicaps = dict(get_current_handicaps())

    # error checking in the GET; probably needed because ob is allowed to use this site
    if len(player_list) != 4:
        return generation_error(
            "You have to select exactly four players. You apparently selected: {}"
            .format(player_list)
        )

    for player in player_list:
        if player not in current_handicaps:
            return generation_error(
                "{} is not in the handicap system."
                .format(player)
            )

    shuffle(player_list)
    if 'Computer' in player_list:
        player_list.remove('Computer')
        player_list.append('Computer')

    if 'Computer' in player_list:
        found_computer = False
        for player in range(4):
            if found_computer:
                if player_list[player] != 'Computer':
                    return generation_error("AI players must be bottom right first.")
            elif player_list[player] == 'Computer':
                found_computer = True

    selections = {
        'players': player_list,
        'team selection': 'random',
        'handicaps before this game': [float(current_handicaps[player]) for player in player_list]
    }

    # team colour selection
    selections['team colours'] = [choice(['blue', 'red'])]
    if selections['team selection'] == 'random':
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

    generation_number = append_generation(selections)

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
