#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from cgi import FieldStorage
from show_game_shared_code import format_time, get_winning_scores, get_result_string, get_net_weight_advantage
from html_tools import html_table, paragraph

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

completed_only = 'completed_only' in GET and GET['completed_only'].value == 'true'

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
	
def get_adjusted_result(gen_number, game_info, results, red_handicap):
    winning_scores = get_winning_scores(
        game_info['team colours'],
        game_info['handicaps before this game']
    )

    total_red_handicap = red_handicap
    if game_info['team colours'][0] == 'red':
        total_red_handicap += player_1_handicap
    else:
        total_red_handicap -= player_1_handicap
    red_team_net_weight_advantage = get_net_weight_advantage(game_info)

    total_red_handicap += red_team_net_weight_advantage * weight_handicap

    if results['red_score'] - total_red_handicap >= winning_scores['to change']['red']:
        return 'red win', red_team_net_weight_advantage
    elif 410 - results['red_score'] + total_red_handicap >= winning_scores['to change']['blue']:
        return 'blue win', red_team_net_weight_advantage
    elif results['red_score'] - total_red_handicap >= winning_scores['to win']['red']:
        return 'red win but no change', red_team_net_weight_advantage
    elif 410 - results['red_score'] + total_red_handicap >= winning_scores['to win']['blue']:
        return 'blue win but no change', red_team_net_weight_advantage
    else:
        return 'perfect draw', red_team_net_weight_advantage


print '''
<html>
<head>
<title>MK8: Winning Margins</title>
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

results_colour = {
    'red win': 0, 'blue win': 0,
    'red win but no change': 0, 'blue win but no change': 0,
    'perfect draw': 0
}

results_position = {
    'player 1 win': 0,
    'player 1 lose': 0,
    'player 1 win but no change': 0,
    'player 1 lose but no change': 0,
    'perfect draw': 0
}

results_position_map_red = {
    'red win': 'player 1 win',
    'blue win': 'player 1 lose',
    'red win but no change': 'player 1 win but no change',
    'blue win but no change': 'player 1 lose but no change',
    'perfect draw': 'perfect draw'
}

results_position_map_blue = {
    'blue win': 'player 1 win',
    'red win': 'player 1 lose', 
    'blue win but no change': 'player 1 win but no change',
    'red win but no change': 'player 1 lose but no change',
    'perfect draw': 'perfect draw'
}

results_weight = {
    'heavier team win': 0,
    'heavier team win but no change': 0,
    'perfect draw': 0,
    'no net weight advantage': 0,
    'lighter team win but no change': 0,
    'lighter team win': 0
}

results_weight_map_red = {
    'red win': 'heavier team win',
    'blue win': 'lighter team win',
    'red win but no change': 'heavier team win but no change',
    'blue win but no change': 'lighter team win but no change',
    'perfect draw': 'perfect draw'
}

results_weight_map_blue = {
    'blue win': 'heavier team win',
    'red win': 'lighter team win',
    'blue win but no change': 'heavier team win but no change',
    'red win but no change': 'lighter team win but no change',
    'perfect draw': 'perfect draw'
}

printed_game_count = 0
for game in game_generations_raw:
    if printed_game_count == display_count:
        break
    gen_number, game_info = eval(game)
    if gen_number in game_results:
        printed_game_count += 1
        result, net_red_weight_advantage = get_adjusted_result(gen_number, game_info, game_results[gen_number], red_handicap)
        results_colour[result] += 1
        if game_info['team colours'][0] == 'red':
            results_position[results_position_map_red[result]] += 1
        else:
            results_position[results_position_map_blue[result]] += 1

        if net_red_weight_advantage == 0:
            results_weight['no net weight advantage'] += 1
        elif net_red_weight_advantage > 0:
            results_weight[results_weight_map_red[result]] += 1
        else:
            results_weight[results_weight_map_blue[result]] += 1


results_table = []

for result in ['red win', 'red win but no change', 'perfect draw', 'blue win but no change', 'blue win']:
    results_table.append([result, results_colour[result]])

print paragraph(html_table(results_table))
print paragraph(
    "win ratio = {}"
    .format(
        round(
            float(results_colour['red win'])/(results_colour['red win'] + results_colour['blue win']),
            2
        )
    )
)
results_table = []

for result in ['player 1 win', 'player 1 win but no change',
               'perfect draw',
               'player 1 lose but no change', 'player 1 lose']:
    results_table.append([result, results_position[result]])

print paragraph(html_table(results_table))
print paragraph(
    "win ratio = {}"
    .format(
        round(
            float(results_position['player 1 win'])/(results_position['player 1 win'] + results_position['player 1 lose']),
            2
        )
    )
)
results_table = []

for result in ['heavier team win', 'heavier team win but no change',
               'perfect draw', 'no net weight advantage',
               'lighter team win but no change', 'lighter team win']:
    results_table.append([result, results_weight[result]])

print paragraph(html_table(results_table))
print paragraph(
    "win ratio = {}"
    .format(
        round(
            float(results_weight['heavier team win'])/(results_weight['heavier team win'] + results_weight['lighter team win']),
            2
        )
    )
)

print '</html>'
