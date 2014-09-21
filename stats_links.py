#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def stats_links():
    links = ['''
<p><a href="show_handicaps.cgi">See current handicaps</a></p>
<p><a href="recent_games.cgi?display_count=10">See previously generated games</a> /
<a href="recent_games.cgi?completed_only=true&display_count=10">
    games with submitted results only</a></p>
<p><a href="result_count.cgi?display_count=100">
    See stats from last 100 games</a> /
    <a href="result_count.cgi?display_count=all">
    or all games ever</a></p> <p> See stats for: ''']

    for category in ['characters', 'vehicles', 'vehicle class', 'tyres', 'gliders']:
        links.append('<a href="result_count.cgi?display_count=all&category={category}">{category}</a>'.format(category=category))

    links.append( ''' (all time) </p> <p> or ''')

    for category in ['weight class', 'speed', 'acceleration', 'weight', 'handling', 'grip']:
        links.append('<a href="result_count.cgi?display_count=all&category={category}">{category}</a>'.format(category=category))

    links.append(''' </p> <p> or ''')

    for category in ['position', 'pairings', 'time of day']:
        links.append('<a href="result_count.cgi?display_count=all&category={category}">{category}</a>'.format(category=category))

    links.append(''' </p> <p> 
<a href='result_count.cgi?display_count=all&separate_team_scores=yes'>average team scores separated by position</a>
<a href='result_count.cgi?display_count=all&separate_team_scores=time'>by time of day</a>
</p> <p> <a href="ian_page.cgi?display_count=100">
    Who has been paired with whom</a></p>
<p><a href="score_distribution.cgi?display_count=all&range_width=5"> See score frequencies for each player </a></p>
<p><a href="http://mariokart.test.lal.cisco.com/cgi-bin/winning_margins.cgi?red_handicap=5&player_1_handicap=2.5&weight_handicap=0.5"> Experimental handicaps for team colour, seat position and weight class</a></p>
<p><a href="wins_by_weight_advantage.cgi?player=1&team_colour=red"> See how often each seat wins depending on weight advantage</a></p>
''')
    return '\n'.join(links)
