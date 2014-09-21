#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from copy import deepcopy as copy

import cgitb
from cgi import FieldStorage

from show_game_shared_code import average, get_adjusted_result
from html_tools import html_table
from mario_kart_files import get_completed_generations_with_results

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

if 'display_count' in GET:
    if GET['display_count'].value == 'all':
        display_count = -1
    else:
        try:
            display_count = int(GET['display_count'].value)
        except ValueError:
            display_count = 10
else:
    display_count = 'all'

if 'red_handicap' in GET:
    red_handicap = float(GET['red_handicap'].value)
else:
    red_handicap = 0

if 'weight_handicap' in GET:
    weight_handicap = float(GET['weight_handicap'].value)
else:
    weight_handicap = 0

if 'player_1_handicap' in GET:
    player_1_handicap = float(GET['player_1_handicap'].value)
else:
    player_1_handicap = 0

if 'player' in GET:
    player_position = int(GET['player'].value)
else:
    player_position = 1

if 'team_colour' in GET:
    team_colour = GET['team_colour'].value
else:
    team_colour = 'red'


weight_class_map = {
    'babyweight': 0,
    'featherweight': 1,
    'lightweight': 2,
    'midweight': 3,
    'cruiserweight': 4,
    'metalweight': 5,
    'heavyweight': 6
}

print '''
<html>
<head>
<title>MK8: Player 1 on the red team</title>
</head>
<style>
.red_team {
    color: red;
}

.blue_team {
    color: blue;
}
</style>'''

generations = get_completed_generations_with_results('all')

results_template = {
    'red win': 0, 'blue win': 0,
    'red win but no change': 0, 'blue win but no change': 0,
    'perfect draw': 0,
    'scores': []
}

results = {
    'total': copy(results_template),
    "-10 to -6": copy(results_template),
    "-5 to -2": copy(results_template),
    "-1 to +1": copy(results_template),
    "2 to 5": copy(results_template),
    "6 to 10": copy(results_template)
}

printed_game_count = 0
for generation in generations:
    if printed_game_count == display_count:
        break

    if ('red score' in generation and
        generation['game info']['team colours'][player_position - 1] == team_colour):
        printed_game_count += 1

        result, net_red_weight_advantage = get_adjusted_result(
            generation,
            red_handicap,
            player_1_handicap,
            weight_handicap
        )

        if net_red_weight_advantage > 5:
            category = "6 to 10"
        elif net_red_weight_advantage > 1:
            category = "2 to 5"
        elif net_red_weight_advantage > -2:
            category = "-1 to +1"
        elif net_red_weight_advantage > -6:
            category = "-5 to -2"
        else:
            category = "-10 to -6"

        if team_colour == 'red':
            score = generation['red score']
        else:
            score = 410 - generation['red_score']

        results[category][result] += 1
        results['total'][result] += 1
        results[category]['scores'].append(score)
        results['total']['scores'].append(score)

result_order_red = ["red win", "red win but no change", "perfect draw", "blue win but no change", "blue win"]
result_order_blue = ["blue win", "blue win but no change", "perfect draw", "red win but no change", "red win"]
results_table = [["weight advantage", "win", "win but no change", "draw", "lose but no change", "lose", "percentage wins", "average score"]]

for weight_advantage in ['-10 to -6', '-5 to -2', '-1 to +1', '2 to 5', '6 to 10', 'total'] :
    results_table.append([weight_advantage])
    if team_colour == 'red':
        result_order = result_order_red
    else:
        result_order = result_order_blue

    for result in result_order:
        results_table[-1].append(results[weight_advantage][result])
    total_outright_wins = results[weight_advantage]['red win'] + results[weight_advantage]['blue win']

    if total_outright_wins == 0:
        results_table[-1].append('n/a')
    else:
        results_table[-1].append(round(float(results[weight_advantage][result_order[0]])/total_outright_wins, 2))

    results_table[-1].append(round(average(results[weight_advantage]['scores']), 1))

print html_table(results_table)

#print results['total']

print '</html>'
