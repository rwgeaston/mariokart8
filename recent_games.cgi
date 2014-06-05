#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from cgi import FieldStorage
from show_game_shared_code import format_time, get_winning_scores, get_result_string

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

if 'completed_only' in GET and GET['completed_only'].value == 'true':
    completed_only = True
else:
    completed_only = False

if 'display_count' in GET:
    try:
        display_count = int(GET['display_count'].value)
    except ValueError:
        display_count = 10
else:
    display_count = 10

def get_teams(game_info):
    teams = {'red':[], 'blue':[]}
    for player, team in zip(game_info['players'], game_info['team colours']):
        teams[team].append(player.capitalize())
    return ("<span class=red_team>{} and {}</span> vs <span class=blue_team>{} and {}</span>"
            .format(teams['red'][0], teams['red'][1], teams['blue'][0], teams['blue'][1]))

def display_completed_game(gen_number, game_info, results):
    scores = ("<span class=red_team>{}</span>-<span class=blue_team>{}</span>"
              .format(results['red_score'], 410-results['red_score']))
    result = get_result_string(
        get_winning_scores(
            game_info['team colours'],
            game_info['handicaps before this game']
        ),
        results['red_score']
    )
    print ('<p>{} {} {} ({}) <a href="show_game.cgi?gen={}">See details.</a> </p>'
           .format(get_teams(game_info), scores, result, format_time(results['time']), gen_number))

def display_non_completed_game(gen_number, game_info):
    print ('<p>{} <a href="show_game.cgi?gen={}">See details or submit result.</a> </p>'
           .format(get_teams(game_info), gen_number))

print '''
<html>
<head>
<title>MK8: Recent games{}</title>
</head>'''.format(' (completed only)' if completed_only else '')

print '''
<style>
.red_team {
    color: red;
}

.blue_team {
    color: blue;
}
</style>'''

with open('generation_log.txt') as generation_log:
    game_generations_raw = generation_log.readlines()

with open('results_log.txt') as results_log:
    game_results_raw = results_log.readlines()

game_results = {}
for result in game_results_raw:
    gen_number, red_score, _, _, time = eval(result)
    game_results[gen_number] = {'red_score': red_score, 'time': time}

game_generations_raw.reverse()

printed_game_count = 0
for game in game_generations_raw:
    if printed_game_count >= display_count:
        break
    gen_number, game_info = eval(game)
    if gen_number in game_results:
        printed_game_count += 1
        display_completed_game(gen_number, game_info, game_results[gen_number])
    elif not completed_only:
        printed_game_count += 1
        display_non_completed_game(gen_number, game_info)

print '</html>'
