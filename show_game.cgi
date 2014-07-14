#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
import os
from cgi import FieldStorage
from show_game_shared_code import show_game_shared, format_time, get_winning_scores, get_result_string, get_net_handicap
from html_tools import html_table

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<title>MK8: Show Random Team Generation</title>
<style>
.red_team {
    color: red;
}

.blue_team {
    color: blue;
}
</style>
</head>
'''

def game_not_played(gen_number):
    print '<form name="submit" action="submit.cgi" method="post">'
    print 'Red team final score: <input type="text" name="redscore"><br><br>'
    print '<input type="hidden" name="gen" value="{}" />'.format(gen_number)
    print '<input type="submit" value="Submit result"></form>'

def show_result(red_score, result_handicaps, winning_scores, time):
    print ("<p>Final score was <span class=red_team>{}</span>-"
           "<span class=blue_team>{}</span> submitted on {}.</p>"
           .format(red_score, 410-red_score, format_time(time)))
    print get_result_string(winning_scores, red_score)

    handicaps_after_this_game = [["Player", "Handicap"]]
    for player, handicap in result_handicaps:
        handicaps_after_this_game.append([player.capitalize(), handicap])

    print '<p>', html_table(handicaps_after_this_game), '</p>'

def handicap_difference_string(red_net_handicap):
    if red_net_handicap == 1:
        return "Red team is better by 1 point per race"
    elif red_net_handicap == -1:
        return "Blue team is better by 1 point per race"
    elif red_net_handicap > 0:
        return "Red team is better by {} points per race".format(red_net_handicap)
    elif red_net_handicap < 0:
        return "Blue team is better by {} points per race".format(-red_net_handicap)
    else:
        return "Handicaps are equal"

def main():
    if 'gen' not in GET:
        print "You don't have a gen value in the GET. How did you get to this page?"
        return

    with open('generation_log.txt') as generation_log:
        for generation in generation_log.readlines():
            gen_number, selection = eval(generation)
            if str(gen_number) == GET['gen'].value:
                break
        else:
            print "I can't find that generation number. How did you get to this page?"
            return

    show_game_shared(selection)

    winning_scores = get_winning_scores(
        selection['team colours'],
        selection['handicaps before this game']
    )

    matching_games = []

    with open('results_log.txt') as results_log:
        for line in results_log.readlines():
            result_gen_number,red_score,_,result_handicaps,time = eval(line)
            if gen_number == result_gen_number:
                matching_games.append((red_score, result_handicaps, time))

    if len(matching_games) == 0:
        tense = 's'
    else:
        tense = 'ed'

    red_net_handicap = get_net_handicap(
        selection['team colours'],
        selection['handicaps before this game']
    )

    print "<p>{}</p>".format(handicap_difference_string(red_net_handicap))

    for team_colour in ['red', 'blue']:
        print ("<p class='{}_team'>"
               "{} team need{} {} to win and {} for handicap to change."
               "</p>"
              .format(team_colour, team_colour.capitalize(), 
                      tense, winning_scores['to win'][team_colour],
                      winning_scores['to change'][team_colour]))

    if len(matching_games) == 0:
        game_not_played(gen_number)
    else:
        if len(matching_games) > 1:
            print "<p>More than one submitted result matches this game generation, wtf? (well here's all the results anyway)</p>"

        for red_score, result_handicaps, time in matching_games:
            show_result(red_score, result_handicaps, winning_scores, time)

    return

main()
