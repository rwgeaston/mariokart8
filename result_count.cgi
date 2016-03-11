#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cgitb
from cgi import FieldStorage
from datetime import datetime

from html_tools import html_table, paragraph
from show_game_shared_code import get_winning_scores, format_time, average
from vehicle_data import characters, spec_order, character_classes, vehicles, \
    tyres, gliders, vehicle_classes
from mario_kart_files import get_completed_generations_with_results, get_current_handicaps
from moon_phase import moon_phase_name

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
    elif GET['separate_team_scores'].value == 'ian':
        show_separate_team_scores = 'ian'
    elif GET['separate_team_scores'].value == 'moon':
        show_separate_team_scores = 'moon'
    elif GET['separate_team_scores'].value == 'shares':
        show_separate_team_scores = 'shares'

sort = 'games played'
if 'sort' in GET:
    if GET['sort'].value in [
        category, 'average team score', 'current handicap',
        'wins', 'draws', 'losses', 'average handicap'
    ]:
        sort = GET['sort'].value
    elif GET['sort'].value == 'category':
        sort = category


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
    elif category == 'weekday':
        return [day_of_the_week(generation['submit time'])]*4
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
    elif category == 'oldscrumteams':
        teams = [get_scrum_team(player) for player in generation['game info']['players']]
        return teams  
    elif category == 'scrumteams':
        teams = [get_new_scrum_team(player) for player in generation['game info']['players']]
        return teams
    elif category == 'moon':
        return [moon_phase_name(generation['submit time'])] * 4
    elif category == 'shares':
        return [simplify_share_prices(generation['share price increase'])] * 4
    else:
        raise Exception("Invalid category value")

def get_scrum_team(player):
    scrum_team_map = {
        'RED': ['Andy', 'Sid', 'Oliver', 'Will', 'Simon', 'Anand'],
        'McFly': ['Ian', 'Guy', 'Shamayl', 'Christina'],
        'Tools': ['Rob', 'Colin', 'Jamie', 'Christian', 'Filla'],
        'Edonus': ['Uma', 'Paulin', 'Gordon', 'Tomg', 'Joe', 'Robh'],
        'Pug': ['Arvinda', 'Martha', 'Thomas'],
        'Transformers': ['Johan', 'Eirik', 'Ben', 'Mate', 'Luca'],
        'Computer': ['Computer'],
        'Media': ['James', 'Gabriel', 'Karlis'],
        'Other': ['Mark', 'Victor', 'Alex', 'Sirisha', 'Lisa'],
    }
    for team, members in scrum_team_map.iteritems():
        if player in members:
            return team
    raise Exception("Don't know what scrum team this person is on: {}".format(player))

def get_new_scrum_team(player):
    scrum_team_map = {
        'Martell': ['Gabriel', 'James', 'Karlis'],
        'Lannister': ['Thomas', 'Simon', 'Guy', 'Filla', 'Mate'],
        'Dayne': ['Rob', 'Uma', 'Tomg', 'Martha', 'Anand'],
        'Stark': ['Sid', 'Sirisha', 'Arvinda', 'Ben'],
        'Wildlings': ['Mark', 'Gordon', 'Joe', 'Johan', 'Eirik', 'Robh', 'Paulin'],
        'X-Wing': ['Andy', 'Will', 'Colin'],
        'Jar-Jar': ['Ian', 'Shamayl'],
        'Computer': ['Computer'],
        'Other': ['Victor', 'Alex', 'Lisa', 'Jamie', 'Christian', 'Luca', 'Oliver', 'Christina'],
    }
    for team, members in scrum_team_map.iteritems():
        if player in members:
            return team
    raise Exception("Don't know what scrum team this person is on: {}".format(player))

def hour(unix_time):
    hour = format_time(unix_time).hour
    return "{} - {}".format(hour, hour + 1)

def day_of_the_week(unix_time):
    return datetime.fromtimestamp(unix_time).strftime('%A')

def simplify_share_prices(price_change):
    if price_change == 'unknown':
        return 'unknown'
    elif price_change < -0.4:
        return 'big drop'
    elif price_change < -0.1:
        return 'small drop'
    elif price_change < 0.1:
        return 'no change'
    elif price_change < 0.4:
        return 'small increase'
    else:
        return 'big increase'



days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
phases_of_the_moon = ['new moon', 'waning crescent', 'waning gibbous', 'full moon', 'waxing gibbous', 'waxing crescent']
share_price_changes = ['unknown', 'big drop', 'small drop', 'no change', 'small increase', 'big increase']

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

        if category != 'players' and player == 'Computer':
            continue

        if category_value not in result_stats:
            result_stats[category_value] = {
                'wins': 0, 'losses': 0, 'draws': 0,
                'red_wins': 0, 'blue_wins': 0,
                'played': 0,
                'red': 0, 'blue': 0,
                'scores': [],
                'scores filtered': {'red': [], 'blue': [], 1: [], 2: [], 3: [], 4: []},
                'scores filtered time': {'Before 1': [], '1-2': [], '2-4': [], '4-6': [], 'After 6': []},
                'scores filtered day': {day: [] for day in days_of_the_week},
                'scores filtered ian watching': {'playing': [], 'watching': [], 'no': []},
                'scores filtered moon': {phase: [] for phase in phases_of_the_moon},
                'scores filtered shares': {change: [] for change in share_price_changes},
                'games_played_without_ian': 0,
            }

        result_stats[category_value]['played'] += 1
        if 'Ian' not in generation['game info']['players']:
            result_stats[category_value]['games_played_without_ian'] += 1
        result_stats[category_value][colour] += 1

        if result == colour:
            result_stats[category_value]['wins'] += 1
            result_stats[category_value][colour + '_wins'] += 1
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

        if generation['ian watched']:
            result_stats[category_value]['scores filtered ian watching']['watching'].append(score_to_log)
        elif 'Ian' in generation['game info']['players']:
            result_stats[category_value]['scores filtered ian watching']['playing'].append(score_to_log)
        else:
            result_stats[category_value]['scores filtered ian watching']['no'].append(score_to_log)

        result_stats[category_value]['scores filtered day'][
            day_of_the_week(generation['submit time'])].append(score_to_log)
        result_stats[category_value]['scores filtered moon'][
            moon_phase_name(generation['submit time'])].append(score_to_log)
        result_stats[category_value]['scores filtered shares'][
            simplify_share_prices(generation['share price increase'])].append(score_to_log)
        
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
    if generation['ian watched']:
        result_stats['ian watched'] += 1


generations = get_completed_generations_with_results(display_count)
current_handicaps = dict(get_current_handicaps())

result_stats = {
    'total games': 0,
    'red team': {'won': 0, 'scores': []},
    'blue team': {'won': 0, 'scores': []},
    'ian watched': 0
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
elif show_separate_team_scores == 'ian':
    results_table[0].extend(["Ian playing", "Ian watching", "Ian in sprint planning"])
    results_table[0].extend(days_of_the_week)
elif show_separate_team_scores == 'moon':
    results_table[0].extend(phases_of_the_moon)
elif show_separate_team_scores == 'shares':
    results_table[0].extend(share_price_changes)
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
for key in ['total games', 'red team', 'blue team', 'ian watched']:
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

def get_games_played(result_stats, player):
    games_played = result_stats[player]['played']
    if player == "Ian":
        games_played = "{} (+ {})".format(games_played, result_stats["ian watched"])
    return games_played

def get_percentage_played(result_stats, player):
    percentage_played = result_stats[player]['played'] * 100 / result_stats['total games']
    if player == "Ian" and "Arvinda" in result_stats:
        percentage_watched_arvinda = result_stats["ian watched"] * 100 / result_stats['total games']
        percentage_played = "{} (+ {})".format(percentage_played, percentage_watched_arvinda)
    return percentage_played

for _, player in players_show_order:
    results_table.append([
        player,
        get_games_played(result_stats, player),
        get_percentage_played(result_stats, player),
    ])

    if show_separate_team_scores == 'yes':
        results_table[-1].append(round(average(result_stats[player]['scores']), 1))
        for filter in ['red', 'blue']:
            wins_this_colour = result_stats[player][filter + '_wins']
            games_this_colour = len(result_stats[player]['scores filtered'][filter])
            percentage_wins_this_colour = 0 if games_this_colour == 0 else wins_this_colour * 100 / games_this_colour
            results_table[-1].append(
                "{} ({}, {})".format(
                    round(average(result_stats[player]['scores filtered'][filter]), 1),
                    games_this_colour,
                    percentage_wins_this_colour,
                )
            )
        for filter in range(1, 5):
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered'][filter]), 1),
                    len(result_stats[player]['scores filtered'][filter]),
                )
            )
    elif show_separate_team_scores == 'ian':
        for ian_watch in ['playing', 'watching', 'no']:
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered ian watching'][ian_watch]), 1),
                    len(result_stats[player]['scores filtered ian watching'][ian_watch])
                )
            )
        for day in days_of_the_week:
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered day'][day]), 1),
                    len(result_stats[player]['scores filtered day'][day])
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
    elif show_separate_team_scores == 'moon':
        for phase in phases_of_the_moon:
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered moon'][phase]), 1),
                    len(result_stats[player]['scores filtered moon'][phase])
                )
            )
    elif show_separate_team_scores == 'shares':
        for change in share_price_changes:
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered shares'][change]), 1),
                    len(result_stats[player]['scores filtered shares'][change])
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
            team.capitalize(),
            result_stats[team + ' team']['won'],
            round(average(result_stats[team + ' team']['scores']), 1),
        )
    )

game_count_message = "There have been {} draws".format(result_stats['total games'] - result_stats['red team']['won'] - result_stats['blue team']['won'])
if display_count == -1:
    game_count_message += " and {} games total".format(result_stats['total games'])
else:
    game_count_message += "."

print paragraph(game_count_message)

if 'debug' in GET:
    print result_stats
