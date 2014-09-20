#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
from cgi import FieldStorage
from html_tools import html_table
from mario_kart_files import get_generations_with_results
from show_game_shared_code import average

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

if 'range size' in GET:
    range_size = int(GET['range size'].value)
else:
    range_size = 10

generations = get_generations_with_results()
red_scores = [generation['red score'] for generation in generations if 'red score' in generation]

red_scores_grouped = [["generation range", "average score"]]

for gen_range_lower in range((len(red_scores) - 1) / range_size + 1):
    score_range = red_scores[gen_range_lower * range_size:(gen_range_lower + 1) * range_size]
    red_scores_grouped.append([
        "{} - {}".format(gen_range_lower * range_size + 1, (gen_range_lower + 1) * range_size),
        average(score_range)
    ])

print html_table(red_scores_grouped)
