#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cgitb
from cgi import FieldStorage
from html_tools import html_table
from mario_kart_files import get_completed_generations_with_results

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


def collate_completed_game(result_stats, generation):
    for player, colour in zip(
        generation['game info']['players'],
        generation['game info']['team colours']
    ):
        if player not in result_stats:
            result_stats[player] = {
                'scores': []
            }

        if colour == 'red':
            result_stats[player]['scores'].append(generation['red score'])
        else:
            result_stats[player]['scores'].append(410 - generation['red score'])

    result_stats['red']['scores'].append(generation['red score'])
    result_stats['blue']['scores'].append(410 - generation['red score'])

generations = get_completed_generations_with_results(display_count)

result_stats = {
    'red': {'scores': []},
    'blue': {'scores': []}
}

for generation in generations:
    collate_completed_game(result_stats, generation)


def count_in_range(result_stats, player, upper, lower):
    count = len([score for score in result_stats[player]['scores'] if lower <= score <= upper])
    if normalised:
        return round(float(count) / len([score for score in result_stats[player]['scores']]) * 100, 1)
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
