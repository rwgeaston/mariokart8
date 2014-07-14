#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from html_tools import html_table
from cgi import FieldStorage
from time import time
from show_game_shared_code import get_winning_scores

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<title>MK8: Submit result</title>
</head>
'''

def invalid_score(message):
    print message.replace('\n', '<br />')
    print ('<br><a href="show_generation.cgi?gen={}">'
           'Return to team generation page.</a>'
           .format(GET['gen'].value))
    return

def handicap_change(selection, change_direction):
    handicaps = []
    with open('players.txt') as current_handicaps:
        for line in current_handicaps:
            player, handicap = line.strip().split(',')
            handicaps.append([player, float(handicap)])

    for player, team in zip(selection['players'], selection['team colours']):
        for person in handicaps:
            if player == person[0]:
                if team == 'red':
                    person[1] += 0.25 * change_direction
                else:
                    person[1] -= 0.25 * change_direction

    # Find AI handicap to set it back to 0
    for person in handicaps:
        if person[0] == 'computer':
            computer_handicap = person[1]
            break
    else:
        raise Exception("Why isn't the computer in the handicaps list?")

    for person in handicaps:
        person[1] -= computer_handicap

    # Need to sort and re-save handicaps
    sorted_handicaps = sorted(handicaps, key=lambda person: -person[1])
    with open('players.txt', 'w') as handicap_file:
        for person in sorted_handicaps:
            handicap_file.write("{},{}\n".format(*person))

def main():
    for key in ['gen', 'redscore']:
        if key not in GET:
            print "You don't have a {} value in the GET. How did you get to this page?".format(key)
            return

    with open('generation_log.txt') as generation_log:
        for generation in generation_log.readlines():
            gen_number, selection = eval(generation)
            if str(gen_number) == GET['gen'].value:
                break
        else:
            print "I can't find that generation number. How did you get to this page?"
            return

    try:
        red_score = int(GET['redscore'].value)
    except ValueError:
        return invalid_score("I don't think you submitted an integer for the red team score.")

    if red_score < 105 or red_score > 305:
        return invalid_score("One of us doesn't know how mario kart scoring works.")

    scores_to_win = get_winning_scores(selection['team colours'], selection['handicaps before this game'])

    if red_score >= scores_to_win['to change']['red']:
        handicap_change(selection, 1)
    elif (410 - red_score) >= scores_to_win['to change']['blue']:
        handicap_change(selection, -1)

    handicaps = []
    with open('players.txt') as current_handicaps:
        for line in current_handicaps:
            player, handicap = line.strip().split(',')
            handicaps.append([player.capitalize(), handicap])

    with open('results_log.txt', 'a') as results_log:
        results_log.write(
            "{},{},{},{},{}\n"
            .format(gen_number,red_score,selection['players'],handicaps,time()))

    return

main()

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
</body>
</html>'''.format(gen_num=GET['gen'].value)
