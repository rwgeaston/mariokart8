#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from standard_page import print_page, get_form_values
from show_game_shared_code import get_winning_scores, format_time, average, \
    get_result, opponents, teammate
from vehicle_data import characters, spec_order, character_classes, vehicles, \
    tyres, gliders, vehicle_classes
from mario_kart_files import get_completed_generations_with_results, get_current_handicaps

form_values = get_form_values([
    ('display_count', -1, int),
    ('category', 'players', str),
    ('column_selection', 'standard', str),
    ('sort', 'games played', str)
])

if (form_values['column_selection'] not in
    ['standard', 'positions', 'time', 'extra_player_stats'] or
    (form_values['column_selection'] == 'extra_player_stats' and
     form_values['category'] != 'players')):
    form_values['column_selection'] = 'standard'

if form_values['sort'] not in [
    form_values['category'], 'average team score', 'current handicap',
    'wins', 'draws', 'losses', 'average handicap'
]:
    form_values['sort'] = form_values['category']


def get_result_raw(winning_scores, red_score):
    return get_result(winning_scores, red_score).split(' ')[0]


def category_map(generation, category):
    if category in ['players', 'vehicles', 'characters',
                    'tyres', 'gliders', ' colours',
                    'handicaps before this game', 'team colours', 'team selection']:
        return generation['game info'][category]
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
        # Seat positions of pairs
        pairings = []
        for player in generation['game info']['players']:
            pairing = [player, teammate(generation['game info'], player)]
            pairing = [generation['game info']['players'].index(player) + 1
                       for player in pairings]
            pairing.sort()
            pairings.append("{} and {}".format(*pairing))
        return pairings
    elif category == 'time of day':
        return [hour(generation['submit time'])]*4
    elif category == 'player pairings':
        # Names of pairs
        pairings = []
        for player in generation['game info']['players']:
            pairing = [player, teammate(generation['game info'], player)]
            pairing.sort()
            pairings.append("{} and {}".format(*pairing))
        return pairings
    else:
        raise Exception("Invalid category value")


def hour(unix_time):
    hour = format_time(unix_time).hour
    return "{} - {}".format(hour, hour + 1)


def collate_completed_game(result_stats, generation, category, column_selection):
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

        if column_selection == 'time':
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
            for stat in ['handicaps', 'teammate handicaps', 'opponent handicaps']:
                if stat not in result_stats[category_value]:
                    result_stats[category_value][stat] = []

            result_stats[category_value]['handicaps'].append(
                dict(generation['handicaps after'])[category_value.capitalize()]
            )

            result_stats[category_value]['teammate handicaps'].append(
                dict(generation['handicaps after'])[teammate(generation['game info'], category_value).capitalize()]
            )

            for opponent in opponents(generation['game info'], category_value):
                result_stats[category_value]['opponent handicaps'].append(
                    dict(generation['handicaps after'])[opponent.capitalize()]
                )

    result_stats['total games'] += 1
    if result == 'red':
        result_stats['red team']['won'] += 1
    elif result == 'blue':
        result_stats['blue team']['won'] += 1
    result_stats['red team']['scores'].append(generation['red score'])
    result_stats['blue team']['scores'].append(410 - generation['red score'])

generations = get_completed_generations_with_results(form_values['display_count'])
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
        form_values['category']
    )

results_table = [[
    form_values['category'], 'games played', 'percentage played',
]]

if form_values['column_selection'] == 'yes':
    results_table[0].extend(['average team score', 'average red team score', 'average blue team score'])
    for player_num in range(1, 5):
        results_table[0].append('average team score when player {}'.format(player_num))
elif form_values['column_selection'] == 'time':
    results_table[0].extend(['Before 1', '1-2', '2-4', '4-6', 'After 6'])
elif form_values['column_selection'] == 'extra_player_statistics':
    results_table[0].extend([
        'current handicap',
        'average handicap',
        'average teammate handicap',
        'average opponent handicap'
    ])
else:
    results_table[0].extend([
        'games on red team', 'games on blue team',
        'wins', 'draws', 'losses',
        'average team score'
    ])

    if form_values['category'] == 'players':
        results_table[0].extend([
            'current handicap',
        ])

players = result_stats.keys()
for key in ['total games', 'red team', 'blue team']:
    players.remove(key)

if form_values['sort'] == 'games played':
    players_show_order = [(-result_stats[player]['played'], player) for player in players]
elif form_values['sort'] == form_values['category']:
    players_show_order = [(player, player) for player in players]
elif form_values['sort'] == 'average team score':
    players_show_order = [(-average(result_stats[player]['scores']), player) for player in players]
elif form_values['sort'] == 'current handicap':
    players_show_order = [(-float(current_handicaps[player]) if player in current_handicaps else player, player) for player in players]
elif form_values['sort'] in ['wins', 'draws', 'losses']:
    players_show_order = [(-result_stats[player][form_values['sort']], player) for player in players]
elif form_values['sort'] == 'average handicap':
    players_show_order = [(-average(result_stats[player]['handicaps']), player) for player in players]

players_show_order.sort()

for _, player in players_show_order:
    results_table.append([
        player,
        result_stats[player]['played'],
        result_stats[player]['played'] * 100 / result_stats['total games'],
    ])

    if form_values['column_selection'] == 'yes':
        results_table[-1].append(round(average(result_stats[player]['scores']), 1))
        for filter in ['red', 'blue'] + range(1, 5):
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered'][filter]), 1),
                    len(result_stats[player]['scores filtered'][filter]),
                )
            )
    elif form_values['column_selection'] == 'time':
        for time_range in ['Before 1', '1-2', '2-4', '4-6', 'After 6']:
            results_table[-1].append(
                "{} ({})".format(
                    round(average(result_stats[player]['scores filtered time'][time_range]), 1),
                    len(result_stats[player]['scores filtered time'][time_range])
                )
            )
    elif form_values['column_selection'] == 'extra_player_stats':
        results_table[-1].extend([
            (current_handicaps[player.capitalize()]
             if player.capitalize() in current_handicaps else '-'),
            round(average(result_stats[player]['handicaps']), 2),
            round(average(result_stats[player]['teammate handicaps']), 2),
            round(average(result_stats[player]['opponent handicaps']), 2),
        ])
    else:
        results_table[-1].extend([
            result_stats[player]['red'],
            result_stats[player]['blue'],
            result_stats[player]['wins'],
            result_stats[player]['draws'],
            result_stats[player]['losses'],
            round(average(result_stats[player]['scores']), 1),
        ])

        if form_values['category'] == 'players':
            results_table[-1].append(
                current_handicaps[player.capitalize()]
                if player.capitalize() in current_handicaps else '-',
            )

page_content = [
    ("table", results_table)
]

for team in ['red', 'blue']:
    page_content.append((
        'text',
        "{} team has won {} times and has had an average team score of {}."
        .format(
            team.capitalize(),
            result_stats[team + ' team']['won'],
            round(average(result_stats[team + ' team']['scores']), 1),
        )
    ))

game_count_message = "There have been {} draws".format(result_stats['total games'] - result_stats['red team']['won'] - result_stats['blue team']['won'])
if form_values['display_count'] == -1:
    game_count_message += " and {} games total".format(result_stats['total games'])
else:
    game_count_message += "."

page_content.append(('text', game_count_message))

print_page("Show result stats", page_content)
