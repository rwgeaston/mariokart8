#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from standard_page import print_page, get_form_values
from show_game_shared_code import get_winning_scores, get_result
from mario_kart_files import get_completed_generations_with_results, get_current_handicaps
from vehicle_data import characters, spec_order, character_classes, vehicles, \
    tyres, gliders, vehicle_classes

form_values = get_form_values([
    ('display_count', -1, int),
])

generations = get_completed_generations_with_results(form_values['display_count'])

def get_result_raw(winning_scores, red_score):
    return get_result(winning_scores, red_score).split(' ')[0]

def map_to_stat(generation, category):
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

generations.reverse()
spec_order_with_order = spec_order.keys()
spec_order_with_order.sort(key=lambda v: spec_order[v])

headings = spec_order_with_order + ["red team flag", "win flag", "team score (centered around 0)", "handicap before game"] 
data = []

for generation in generations:

    winning_scores = get_winning_scores(
        generation['game info']['team colours'],
        generation['game info']['handicaps before this game']
    )
    result = get_result_raw(
        winning_scores,
        generation['red score'],
    )

    red_score = generation['red score'] - 205
    blue_score = - red_score

    specs_this_generation = {}
    for spec in spec_order:
        specs_this_generation[spec] = map_to_stat(generation, spec)

    for player in range(4):
        colour = generation['game info']['team colours'][player]
        spec_this_player = []
        
        for spec in spec_order_with_order:
            spec_this_player.append((specs_this_generation[spec][player] - 1) / 4.75)

        spec_this_player.append(int(colour=='red'))
        spec_this_player.append(int(colour == result))
        spec_this_player.append(red_score if colour == 'red' else blue_score)
        spec_this_player.append(generation['game info']['handicaps before this game'][player])

        data.append(spec_this_player)

page_content = []

def get_column(num, filter_function=None):
    if filter_function:
        data_to_use = filter(filter_function, data)
    else:
        data_to_use = data
    return [row[num] for row in data_to_use]

import numpy

def readable(regression_result, accuracy, labels=None):
   coefficients, covariants = regression_result
   if not labels:
       labels = spec_order_with_order
   rounded_coefficients = [round(coefficient, accuracy) for coefficient in coefficients]
   return (
        "{} + ".format(rounded_coefficients[0]) + 
        " + ".join(["{}*{}".format(value, stat) for value, stat in zip(rounded_coefficients[1:], labels)]) +
        " (std dev {})".format([round(value, accuracy) for value in numpy.sqrt(numpy.diag(covariants))])
    )

from scipy.optimize import curve_fit
import scipy

def linear_fn(inputs, constant, a, b, c, d, e):
    coefficients = [a, b, c, d, e]
    return constant + sum([coefficient * variable for coefficient, variable in zip(coefficients, inputs)])

def linear_fn2(inputs, constant, a, b):
    coefficients = [a, b]
    return constant + sum([coefficient * variable for coefficient, variable in zip(coefficients, inputs)])

def linear_fn3(inputs, constant, a, b, c):
    coefficients = [a, b]
    return constant + sum([coefficient * variable for coefficient, variable in zip(coefficients, inputs)])

def linear_fn1(inputs, constant, a):
    return constant + a * inputs[0]

def print_regressions(filter_function):
    stats = scipy.array([get_column(i, filter_function) for i in range(5)])
    wins = scipy.array(get_column(6, filter_function))
    scores = scipy.array(get_column(7, filter_function))
    colours = scipy.array(get_column(5, filter_function))

    r = curve_fit(linear_fn, stats, scores)
    page_content.append(('text', "Best fit for average score is {}".format(readable(r, 1))))
    r = curve_fit(linear_fn, stats, wins)
    page_content.append(('text', "Best fit for win percentage is {}".format(readable(r, 2))))

    r = curve_fit(linear_fn2, stats[:2], scores)
    page_content.append(('text', "Best simplified fit for average score is {}".format(readable(r, 1))))
    r = curve_fit(linear_fn2, stats[:2], wins)
    page_content.append(('text', "Best simplified fit for win percentage is {}".format(readable(r, 2))))

    r = curve_fit(linear_fn1, stats[:1], scores)
    page_content.append(('text', "Best speed only fit for average score is {}".format(readable(r, 1))))
    r = curve_fit(linear_fn1, stats[:1], wins)
    page_content.append(('text', "Best speed only fit for win percentage is {}".format(readable(r, 2))))

    r = curve_fit(linear_fn1, stats[2:3], scores)
    page_content.append((
        'text', 
        "Best weight only fit for average score is {}".format(readable(r, 1, ['weight']))
    ))
    r = curve_fit(linear_fn1, stats[2:3], wins)
    page_content.append((
        'text',
        "Best weight only fit for win percentage is {}".format(readable(r, 2, ['weight']))
    ))

    r = curve_fit(linear_fn2, [stats[0], stats[2]], scores)
    page_content.append((
        'text',
        "Best speed and weight fit for average score is {}".format(readable(r, 1, ['speed', 'weight']))
    ))
    r = curve_fit(linear_fn2, [stats[0], stats[2]], wins)
    page_content.append((
        'text',
        "Best speed and weight fit for win percentage is {}".format(readable(r, 2, ['speed', 'weight']))
    ))

def blank_filter_function(row):
    return True

print_regressions(blank_filter_function)

page_content.append(('important text', "Now only looking at players with handicap >= 7."))

def high_handicap_filter(row):
    return row[8] >= 7

print_regressions(high_handicap_filter)

page_content.append(('important text', "Looking at red team only."))

def red_team(row):
    return bool(row[5])

def blue_team(row):
    return not red_team(row)

print_regressions(red_team)

page_content.append(('important text', "Looking at blue team only."))

print_regressions(blue_team)

page_content.append(('text', "This was based on the data:"))
page_content.append(('table', [headings] + data))
print_page("Stat and score correlations", page_content)

