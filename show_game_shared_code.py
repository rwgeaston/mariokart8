#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from html_tools import html_table, paragraph
import vehicle_data
from time import localtime
from math import ceil
from datetime import datetime
from vehicle_data import characters


def average(a_list):
    if len(a_list) == 0:
        return 0
    return sum([float(value) for value in a_list])/len(a_list)


def show_selection(selection, player_number):
    return '''
<p class='{team_colour}_team'>
{player}<br />
{character}<br />
{vehicle}<br />
{tyres}<br />
{glider}<br /></p>'''.format(
        player=selection['players'][player_number].capitalize(),
        team_colour=selection['team colours'][player_number],
        character=selection['characters'][player_number],
        vehicle=selection['vehicles'][player_number],
        tyres=selection['tyres'][player_number],
        glider=selection['gliders'][player_number]
    )

def selection_stats(selection, player_number):
    weight_class = vehicle_data.characters[selection['characters'][player_number]]
    player_stats = vehicle_data.character_classes[weight_class]
    vehicle_stats = vehicle_data.vehicles[selection['vehicles'][player_number]]
    tyre_stats = vehicle_data.tyres[selection['tyres'][player_number]]
    glider_stats = vehicle_data.gliders[selection['gliders'][player_number]]
    overall_stats = map(sum, zip(player_stats, vehicle_stats, tyre_stats, glider_stats))
    overall_stats_strings = [str(element) for element in overall_stats]
    return ["<p class='{team_colour}_team'>{player_name}</p>"
            .format(
                team_colour=selection['team colours'][player_number],
                player_name=selection['players'][player_number].capitalize()),
            str(selection['handicaps before this game'][player_number])] + \
            overall_stats_strings

def show_game_shared(selection):
    print html_table([
        [show_selection(selection, 0), show_selection(selection, 1)],
        [show_selection(selection, 2), show_selection(selection, 3)]
    ])

    print '<br />'

    print html_table(
        [['Player', 'Handicap', 'Speed', 'Accel', 'Weight', 'Handling', 'Grip']] +
        [selection_stats(selection, player_number) for player_number in range(4)]
    )

def get_winning_scores(team_colours, handicaps):
    net_red_handicap = get_net_handicap(team_colours, handicaps)
    winning_scores = get_winning_scores_raw(net_red_handicap)
    for result in ['to win', 'to change']:
        for colour in ['red', 'blue']:
            winning_scores[result][colour] = int(ceil(winning_scores[result][colour]))
    return winning_scores

def get_winning_scores_raw(net_red_handicap):
    return {
        'to win':{
            'red': 205 + net_red_handicap * 5 / 2.0 + 0.25,
            'blue': 205 - net_red_handicap * 5 / 2.0 + 0.25
        },
        'to change':{
            'red': 205 + net_red_handicap * 5 / 2.0 + 2.5,
            'blue': 205 - net_red_handicap * 5 / 2.0 +2.5
        }
    }

def get_net_handicap(team_colours, handicaps):
    net_red_handicap = 0
    for player_num in range(4):
        if team_colours[player_num] == 'red':
            net_red_handicap += handicaps[player_num]
        else:
            net_red_handicap -= handicaps[player_num]
    return net_red_handicap

def format_time(unix_time):
    time_split = localtime(unix_time)
    return datetime(
        time_split.tm_year,
        time_split.tm_mon,
        time_split.tm_mday,
        time_split.tm_hour,
        time_split.tm_min,
        time_split.tm_sec
    )

def get_result(winning_scores, red_score):
    if red_score >= winning_scores['to change']['red']:
        return "red"
    elif 410 - red_score >= winning_scores['to change']['blue']:
        return "blue"
    elif red_score >= winning_scores['to win']['red']:
        return "red no change"
    elif 410 - red_score >= winning_scores['to win']['blue']:
        return "blue no change"
    else:
        return "draw"

def get_winning_margin(winning_scores, net_red_handicap, red_score):
    result = get_result(winning_scores, red_score)
    net_score = red_score * 2 - net_red_handicap * 5 - 410
    if 'red' in result:
        return net_score
    elif 'blue' in result:
        return - net_score
    else:
        return 0

def get_winning_margin_string(winning_scores, net_red_handicap, red_score):
    result = get_result(winning_scores, red_score)
    if result == 'draw':
        return ""
    elif 'red' in result:
        return "Red team wins by {} points".format(get_winning_margin(winning_scores, net_red_handicap, red_score))
    else:
        return "Blue team wins by {} points".format(get_winning_margin(winning_scores, net_red_handicap, red_score))

def get_result_string(winning_scores, red_score):
    pretty_strings = {
        'red': 'Red team is the best!',
        'blue': 'Blue team is the best!',
        'blue no change': 'Blue team is the best, but no handicap change.',
        'red no change': 'Red team is the best, but no handicap change.',
        'draw': "It's a draw!",
    }
    return pretty_strings[get_result(winning_scores, red_score)]

weight_class_map = {
    'babyweight': 0,
    'featherweight': 1,
    'lightweight': 2,
    'midweight': 3,
    'cruiserweight': 4,
    'metalweight': 5,
    'heavyweight': 6
}


def get_net_weight_advantage(game_info):
    red_team_net_weight_advantage = 0
    for character, colour in zip(game_info['characters'], game_info['team colours']):
        weight_this_character = weight_class_map[characters[character]]
        if colour == 'red':
            red_team_net_weight_advantage += weight_this_character
        else:
            red_team_net_weight_advantage -= weight_this_character

    return red_team_net_weight_advantage


def get_result_extra_handicaps(game_info, red_score):
    net_red_handicap = get_net_handicap(game_info['team colours'], game_info['handicaps before this game'])
    additional_handicap = 1
    if game_info['team colours'][0] == 'red':
        additional_handicap += 0.5
    else:
        additional_handicap -= 0.5

    additional_handicap += 0.1 * get_net_weight_advantage(game_info)

    net_red_handicap += additional_handicap

    winning_scores = get_winning_scores_raw(net_red_handicap)
    result = get_result(winning_scores, red_score)
    margin = get_winning_margin(winning_scores, net_red_handicap, red_score)

    if result == 'draw':
        result_string = "With this adjustment game would have been a perfect draw"
    elif result == 'red':
        result_string = "With this adjustment, red team would have won by {}".format(margin)
    elif result == 'blue':
        result_string = "With this adjustment, blue team would have won by {}".format(margin)
    elif result == 'red no change':
        result_string = "With this adjustment, red team would have won by {} so no handicap change".format(margin)
    else:
        result_string = "With this adjustment, blue team would have won by {} so no handicap change".format(margin)

    return paragraph(
        "Red team additional handicap with colour/positions/weight class adjustment of 1, 0.5, 0.1 is {}."
        .format(additional_handicap)
    ) + paragraph(
        result_string
    )


def get_adjusted_result(generation, red_handicap, player_1_handicap, weight_handicap):
    winning_scores = get_winning_scores(
        generation['game info']['team colours'],
        generation['game info']['handicaps before this game']
    )

    total_red_handicap = red_handicap
    if generation['game info']['team colours'][0] == 'red':
        total_red_handicap += player_1_handicap
    else:
        total_red_handicap -= player_1_handicap

    red_team_net_weight_advantage = get_net_weight_advantage(generation['game info'])
    total_red_handicap += red_team_net_weight_advantage * weight_handicap

    if generation['red score'] - total_red_handicap >= winning_scores['to change']['red']:
        return 'red win', red_team_net_weight_advantage
    elif 410 - generation['red score'] + total_red_handicap >= winning_scores['to change']['blue']:
        return 'blue win', red_team_net_weight_advantage
    elif generation['red score'] - total_red_handicap >= winning_scores['to win']['red']:
        return 'red win but no change', red_team_net_weight_advantage
    elif 410 - generation['red score'] + total_red_handicap >= winning_scores['to win']['blue']:
        return 'blue win but no change', red_team_net_weight_advantage
    else:
        return 'perfect draw', red_team_net_weight_advantage
