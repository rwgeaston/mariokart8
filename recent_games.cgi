#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb

from cgi import FieldStorage
from show_game_shared_code import format_time, get_winning_scores, get_result_string
from mario_kart_files import get_completed_generations_with_results, get_generations_with_results

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
    display_count = 10


def get_teams(game_info):
    teams = {'red': [], 'blue': []}
    for player, team in zip(game_info['players'], game_info['team colours']):
        teams[team].append(player)
    return ("<span class=red_team>{} and {}</span> vs <span class=blue_team>{} and {}</span>"
            .format(teams['red'][0], teams['red'][1], teams['blue'][0], teams['blue'][1]))


def display_completed_game(generation):
    scores = (
        "<span class=red_team>{}</span>-<span class=blue_team>{}</span>"
        .format(
            generation['red score'],
            410 - generation['red score']
        )
    )

    result = get_result_string(
        get_winning_scores(
            generation['game info']['team colours'],
            generation['game info']['handicaps before this game']
        ),
        generation['red score']
    )
    print (
        '<p>{} {} {} ({}) <a href="show_game.cgi?gen={}">See details.</a> </p>'
        .format(
            get_teams(generation['game info']),
            scores,
            result,
            format_time(generation['submit time']),
            generation['generation number']
        )
    )


def display_non_completed_game(generation):
    text = '{} '.format(get_teams(generation['game info']))
    if 'time' in generation['game info']:
        text += '({}) '.format(format_time(generation['game info']['time']))
    print (
        '<p>{}<a href="show_game.cgi?gen={}">See details or submit result.</a> </p>'
        .format(text, generation['generation number'])
    )

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

if completed_only:
    generations = get_completed_generations_with_results(display_count)
else:
    generations = get_generations_with_results(display_count)

for generation in generations:

    if 'red score' in generation:
        display_completed_game(generation)
    elif not completed_only:
        display_non_completed_game(generation)

print '</html>'
