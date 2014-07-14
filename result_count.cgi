#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from cgi import FieldStorage
from html_tools import html_table
from show_game_shared_code import get_winning_scores

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<script src="sorttable.js"></script>
<title>MK8: Show result stats</title>
</head>
'''

if 'display_count' in GET:
    if GET['display_count'].value == 'all':
        display_count = -1
    else:
        try:
            display_count = int(GET['display_count'].value)
        except ValueError:
            display_count = 100
else:
    display_count = 100

def average(a_list):
    return sum(a_list)/len(a_list)

def get_result_raw(winning_scores, red_score):
    if red_score >= winning_scores['to change']['red']:
        return "red"
    elif 410 - red_score >= winning_scores['to change']['blue']:
        return "blue"
    else:
        return "draw"

def collate_completed_game(result_stats, gen_number, game_info, game_results):
    result = get_result_raw(
        get_winning_scores(
            game_info['team colours'],
            game_info['handicaps before this game']
        ),
        game_results['red_score']
    )
    for player, colour in zip(game_info['players'], game_info['team colours']):
        if player not in result_stats:
            result_stats[player] = {
                'wins': 0, 'losses': 0, 'draws': 0,
                'played': 0,
                'red': 0, 'blue': 0,
                'scores': []
            }

        result_stats[player]['played'] += 1
        result_stats[player][colour] += 1

        if result == colour:
            result_stats[player]['wins'] += 1
        elif result == 'draw':
            result_stats[player]['draws'] += 1
        else:
            result_stats[player]['losses'] += 1

        if colour == 'red':
            result_stats[player]['scores'].append(game_results['red_score'])
        else:
            result_stats[player]['scores'].append(410 - game_results['red_score'])

    result_stats['total games'] += 1

with open('generation_log.txt') as generation_log:
    game_generations_raw = generation_log.readlines()

with open('results_log.txt') as results_log:
    game_results_raw = results_log.readlines()

with open('players.txt') as current_handicaps_file:
    current_handicaps_lines = current_handicaps_file.readlines()

current_handicaps = {}
for line in current_handicaps_lines:
    player, handicap = line.strip().split(',')
    current_handicaps[player] = handicap

game_results = {}
for result in game_results_raw:
    gen_number, red_score, _, _, time = eval(result)
    game_results[gen_number] = {'red_score': red_score, 'time': time}

game_generations_raw.reverse()

result_stats = {'total games': 0}

printed_game_count = 0
for game in game_generations_raw:
    if printed_game_count == display_count:
        break
    gen_number, game_info = eval(game)
    if gen_number in game_results:
        printed_game_count += 1
        collate_completed_game(result_stats, gen_number, game_info, game_results[gen_number])

results_table = [[
    'player', 'games played', 'percentage played',
    'wins', 'draws', 'losses', 'games on red team',
    'games on blue team', 'average team score', 'current handicap'
]]

players = result_stats.keys()
players.remove('total games')
playcount_and_players = [(-result_stats[player]['played'], player) for player in players]
playcount_and_players.sort()

for _, player in playcount_and_players:
    results_table.append([
        player,
        result_stats[player]['played'],
        result_stats[player]['played'] * 100 / result_stats['total games'],
        result_stats[player]['wins'],
        result_stats[player]['draws'],
        result_stats[player]['losses'],
        result_stats[player]['red'],
        result_stats[player]['blue'],
        average(result_stats[player]['scores']),
        current_handicaps[player]
    ])

print html_table(results_table, sortable=True)
