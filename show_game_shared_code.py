#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from html_tools import html_table
import vehicle_data
from time import localtime
from math import ceil
from datetime import datetime

def show_selection(selection, player_number):
    return '''
<p class='{team_colour}_team'>
{character}<br />
{vehicle}<br />
{tyres}<br />
{glider}<br /></p>'''.format(
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
    return {
        'to win':{
            'red': int(ceil(205 + net_red_handicap * 5 / 2.0 + 0.25)),
            'blue': int(ceil(205 - net_red_handicap * 5 / 2.0 + 0.25))
        },
        'to change':{
            'red': int(ceil(205 + net_red_handicap * 5 / 2.0 + 2.5)),
            'blue': int(ceil(205 - net_red_handicap * 5 / 2.0 +2.5))
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

def get_result_string(winning_scores, red_score):
    if red_score >= winning_scores['to change']['red']:
        return "Red team is the best!"
    elif 410 - red_score >= winning_scores['to change']['blue']:
        return "Blue team is the best!"
    elif red_score >= winning_scores['to win']['red']:
        return "Red team wins, but no handicap change."
    elif 410 - red_score >= winning_scores['to win']['blue']:
        return "Blue team wins, but no handicap change."
    else:
        return "It's a draw!"