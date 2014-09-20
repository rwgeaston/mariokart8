#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from cgi import FieldStorage
from html_tools import html_table, paragraph
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
<title>MK8: Show score distribution</title>
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

if 'range_width' in GET:
    try:
        range_width = int(GET['range_width'].value)
    except ValueError:
        range_width = 5
else:
    range_width = 5

if 'normalised' in GET:
    normalised = True
else:
    normalised = False


def collate_completed_game(result_stats, gen_number, game_info, game_results):
    for player, colour in zip(game_info['players'], game_info['team colours']):
        if player not in result_stats:
            result_stats[player] = {
                'scores': []
            }

        if colour == 'red':
            result_stats[player]['scores'].append(game_results['red_score'])
        else:
            result_stats[player]['scores'].append(410 - game_results['red_score'])

    result_stats['red']['scores'].append(game_results['red_score'])
    result_stats['blue']['scores'].append(410 - game_results['red_score'])

with open('generation_log.txt') as generation_log:
    game_generations_raw = generation_log.readlines()

with open('results_log.txt') as results_log:
    game_results_raw = results_log.readlines()

with open('players.txt') as current_handicaps_file:
    current_handicaps_lines = current_handicaps_file.readlines()

game_results = {}
for result in game_results_raw:
    gen_number, red_score, _, _, time = eval(result)
    game_results[gen_number] = {'red_score': red_score, 'time': time}

game_generations_raw.reverse()

result_stats = {
    'red': {'scores': []}, 
    'blue': {'scores': []}
}


printed_game_count = 0
for game in game_generations_raw:
    if printed_game_count == display_count:
        break
    gen_number, game_info = eval(game)
    if gen_number in game_results:
        printed_game_count += 1
        collate_completed_game(result_stats, gen_number, game_info, game_results[gen_number])


def count_in_range(result_stats, player, upper, lower):
    count = len([score for score in result_stats[player]['scores'] if lower <= score <= upper])
    if normalised:
        return round(float(count) /  len([score for score in result_stats[player]['scores']]) * 100, 1)
    else:
        return count

players = result_stats.keys()
players.sort()
players.remove('red')
players.remove('blue')

table_headings = ['range', 'red', 'blue'] + players
table = [table_headings]
for lower in xrange(120, 290, range_width):
    upper = lower + range_width - 1
    table.append(["{}-{}".format(lower, upper)])
    for player in ['red', 'blue'] + players:
        table[-1].append(count_in_range(result_stats, player, upper, lower))

print html_table(table)
    
    
