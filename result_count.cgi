#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cgitb
from cgi import FieldStorage

from html_tools import html_table, paragraph
from show_game_shared_code import get_winning_scores, format_time, average
from vehicle_data import characters, spec_order, character_classes, vehicles, \
    tyres, gliders, vehicle_classes
from mario_kart_files import get_completed_generations_with_results, get_current_handicaps

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

if 'category' in GET:
    category = GET['category'].value
else:
    category = 'players'

show_separate_team_scores = False
if 'separate_team_scores' in GET:
    if GET['separate_team_scores'].value in ['yes', 'true']:
        show_separate_team_scores = 'yes'
    elif GET['separate_team_scores'].value == 'time':
        show_separate_team_scores = 'time'

sort = 'games played'
if 'sort' in GET:
    if GET['sort'].value in [
        category, 'average team score', 'current handicap',
        'wins', 'draws', 'losses', 'average handicap'
    ]:
        sort = GET['sort'].value


def get_result_raw(winning_scores, red_score):
    if red_score >= winning_scores['to change']['red']:
        return "red"
    elif 410 - red_score >= winning_scores['to change']['blue']:
        return "blue"
    else:
        return "draw"


def category_map(generation, category):
    if category in ['players', 'vehicles', 'characters',
                    'tyres', 'gliders', ' colours',
                    'handicaps before this game', 'team colours', 'team selection']:
        return [value for value in generation['game info'][category]]
    elif category == 'weight class':
        # characters is the map from characters to weight classes
        return [characters[character] for character in generation['game info']['characters']]
    elif category in spec_order:
        spec_position = spec_order[category]
        weight_classes = [character_classes[characters[character]] for character in generation['game info']['characters']]
        stat_per_player = []
        for weight_class, vehicle, tyre, glider in zip(
            weight_classes,
            generation['game info']['vehicles'],
            generation['game info']['tyres'],
            generation['game info']['gliders']
        ):
            vehicle_stats = vehicles[vehicle]
            tyre_stats = tyres[tyre]
            glider_stats = gliders[glider]
            stat_this_player = sum(
                [factor[spec_position] for factor in
                    [weight_class, vehicle_stats, tyre_stats, glider_stats]]
            )
            stat_per_player.append(stat_this_player)
        return stat_per_player
    elif category == 'vehicle class':
        return [vehicle_classes[vehicle] for vehicle in generation['game info']['vehicles']]
    elif category == 'position':
        return range(1, 5)
    elif category == 'pairings':
        pairings = []
        for player, colour in zip(range(4), generation['game info']['team colours']):
            for potential_teammate in range(4):
                if player != potential_teammate:
                    if generation['game info']['team colours'][potential_teammate] == colour:
                        pairing_players = [player + 1, potential_teammate + 1]
                        pairing_players.sort()
                        pairings.append("{} and {}".format(*pairing_players))
        return pairings
    elif category == 'time of day':
        return [hour(generation['submit time'])]*4
    elif category == 'player pairings':
        pairings = []
        for player, player_name, colour in zip(
            range(4),
            generation['game info']['players'],
            generation['game info']['team colours']
        ):
            for potential_teammate, teammate_name in zip(
                range(4),
                generation['game info']['players']
            ):
                if player != potential_teammate:
                    if generation['game info']['team colours'][potential_teammate] == colour:
                        pairing_players = [player_name, teammate_name]
                        pairing_players.sort()
                        pairings.append("{} and {}".format(*pairing_players))
        return pairings
    else:
        raise Exception("Invalid category value")


def hour(unix_time):
    hour = format_time(unix_time).hour
    return "{} - {}".format(hour, hour + 1)


def collate_completed_game(result_stats, generation, category):
    result = get_result_raw(
        get_winning_scores(
            generation['game info']['team colours'],
            generation['game info']['handicaps before this game']
        ),
        generation['red score']
    )
    for player_num, player, category_value, colour in zip(
        xrange(1, 5), generation['game info']['players'],
        category_map(generation, category),
        generation['game info']['team colours']
    ):
        # category_value typically player name but page can be hacked to do other things

        if category != 'players' and player == 'computer':
            continue

        if category_value not in result_stats:
            result_stats[category_value] = {
                'wins': 0, 'losses': 0, 'draws': 0,
                'played': 0,
                'red': 0, 'blue': 0,
                'scores': [],
                'scores filtered': {'red': [], 'blue': [], 1: [], 2: [], 3: [], 4: []},
                'scores filtered time': {'Before 1': [], '1-2': [], '2-4': [], '4-6': [], 'After 6': []}
            }

        result_stats[category_value]['played'] += 1
        result_stats[category_value][colour] += 1

        if result == colour:
            result_stats[category_value]['wins'] += 1
        elif result == 'draw':
            result_stats[category_value]['draws'] += 1
        else:
            result_stats[category_value]['losses'] += 1

        if colour == 'red':
            score_to_log = generation['red score']
        else:
            score_to_log = 410 - generation['red score']

        result_stats[category_value]['scores'].append(score_to_log)
        result_stats[category_value]['scores filtered'][colour].append(score_to_log)
        result_stats[category_value]['scores filtered'][player_num].append(score_to_log)

        if show_separate_team_scores == 'time':
            time_played = int(hour(generation['submit time']).split(' ')[0])
            if time_played < 13:
                time_played_category = "Before 1"
            elif time_played > 17:
                time_played_category = "After 6"
            else:
                time_played_start_range = time_played - 12 - (time_played % 2)
                time_played_end_range = time_played_start_range + 2
                if time_played_start_range <= 1:
                    time_played_start_range = 1
                time_played_category = "{}-{}".format(time_played_start_range, time_played_end_range)
            result_stats[category_value]['scores filtered time'][time_played_category].append(score_to_log)

        if category == 'players':
            if 'handicaps' not in result_stats[category_value]:
                result_stats[category_value]['handicaps'] = []
            result_stats[category_value]['handicaps'].append(
                dict(generation['handicaps after'])[category_value]
            )

    result_stats['total games'] += 1
    if result == 'red':
        result_stats['red team']['won'] += 1
    elif result == 'blue':
        result_stats['blue team']['won'] += 1
    result_stats['red team']['scores'].append(generation['red score'])
    result_stats['blue team']['scores'].append(410 - generation['red score'])

generations = get_completed_generations_with_results(display_count)
current_handicaps = dict(get_current_handicaps())

result_stats = {
    'total games': 0,
    'red team': {'won': 0, 'scores': []},
    'blue team': {'won': 0, 'scores': []}
}

printed_game_count = 0
for generation in generations:
    collate_completed_game(
        result_stats,
        generation,
        category
    )

results_table = [[
    category, 'games played', 'percentage played',
]]

if show_separate_team_scores == 'yes':
    results_table[0].extend(['average team score', 'average red team score', 'average blue team score'])
    for player_num in range(1, 5):
        results_table[0].append('average team score when player {}'.format(player_num))
elif show_separate_team_scores == 'time':
    results_table[0].extend(['Before 1', '1-2', '2-4', '4-6', 'After 6'])
else:
    results_table[0].extend([
        'games on red team', 'games on blue team',
        'wins', 'draws', 'losses',
        'average team score'
    ])

    if category == 'players':
        results_table[0].extend([
            'current handicap', 'average handicap'
        ])

players = result_stats.keys()
for key in ['total games', 'red team', 'blue team']:
    players.remove(key)
if sort == 'games played':
    players_show_order = [(-result_stats[player]['played'], player) for player in players]
elif sort == category:
    players_show_order = [(player, player) for player in players]
elif sort == 'average team score':
    players_show_order = [(-average(result_stats[player]['scores']), player) for player in players]
elif sort == 'current handicap':
    players_show_order = [(-float(current_handicaps[player]) if player in current_handicaps else player, player) for player in players]
elif sort in ['wins', 'draws', 'losses']:
    players_show_order = [(-result_stats[player][sort], player) for player in players]
elif sort == 'average handicap':
    players_show_order = [(-average(result_stats[player]['handicaps']), player) for player in players]

players_show_order.sort()

for _, player in players_show_order:
    results_table.append([
        player,
        result_stats[player]['played'],
        result_stats[player]['played'] * 100 / result_stats['total games'],
    ])

    if show_separate_team_scores == 'yes':
        results_table[-1].append(round(average(result_stats[player]['scores']), 1))
        for filter in ['red', 'blue'] + range(1, 5):
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered'][filter]), 1),
                    len(result_stats[player]['scores filtered'][filter]),
                )
            )
    elif show_separate_team_scores == 'time':
        for time_range in ['Before 1', '1-2', '2-4', '4-6', 'After 6']:
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered time'][time_range]), 1),
                    len(result_stats[player]['scores filtered time'][time_range])
                )
            )
    else:
        results_table[-1].extend([
            result_stats[player]['red'],
            result_stats[player]['blue'],
            result_stats[player]['wins'],
            result_stats[player]['draws'],
            result_stats[player]['losses'],
            round(average(result_stats[player]['scores']), 1),
        ])

        if category == 'players':
            results_table[-1].extend([
                current_handicaps[player] if player in current_handicaps else '-',
                round(average(result_stats[player]['handicaps']), 2),
        ])

print html_table(results_table, sortable=True)

for team in ['red', 'blue']:
    print paragraph(
        "{} team has won {} times and has had an average team score of {}."
        .format(
            team,
            result_stats[team.capitalize() + ' team']['won'],
            round(average(result_stats[team + ' team']['scores']), 1),
        )
    )

game_count_message = "There have been {} draws".format(result_stats['total games'] - result_stats['red team']['won'] - result_stats['blue team']['won'])
if display_count == -1:
    game_count_message += " and {} games total".format(result_stats['total games'])
else:
    game_count_message += "."

print paragraph(game_count_message)
