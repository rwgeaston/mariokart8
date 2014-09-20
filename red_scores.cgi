#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from cgi import FieldStorage
from html_tools import html_table, paragraph
from show_game_shared_code import get_winning_scores, format_time

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

if 'range size' in GET:
    range_size = int(GET['range size'].value)
else:
    range_size = 10

with open('results_log.txt') as results_log:
    game_results_raw = results_log.readlines()

red_scores = []
for game in game_results_raw:
    score = eval(game)[1]
    red_scores.append(score)

red_scores_grouped = [["generation range", "average score"]]

def average(a_list):
    return round(sum([float(value) for value in a_list])/len(a_list), 1)

for gen_range_lower in range((len(red_scores) - 1) / range_size + 1):
    score_range = red_scores[gen_range_lower * range_size:(gen_range_lower + 1) * range_size]
    red_scores_grouped.append([
        "{} - {}".format(gen_range_lower * range_size + 1, (gen_range_lower + 1) * range_size),
        average(score_range)
    ])

print html_table(red_scores_grouped)
