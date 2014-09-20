#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
from cgi import FieldStorage

from show_game_shared_code import show_game_shared, format_time, \
    get_winning_scores, get_result_string, get_net_handicap, \
    get_winning_margin_string, get_result_extra_handicaps
from html_tools import html_table, paragraph
from mario_kart_files import get_one_generation_from_gen_number

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


def show_result(red_score, result_handicaps, winning_scores, time, game_info, net_red_handicap):
    print ("<p>Final score was <span class=red_team>{}</span>-"
           "<span class=blue_team>{}</span> submitted on {}.</p>"
           .format(red_score, 410-red_score, format_time(time)))

    print paragraph(get_winning_margin_string(winning_scores, net_red_handicap, red_score))
    print paragraph(get_result_string(winning_scores, red_score))

    print get_result_extra_handicaps(game_info, red_score)

    handicaps_after_this_game = [["Player", "Handicap"]]
    for player, handicap in result_handicaps:
        handicaps_after_this_game.append([player.capitalize(), handicap])

    print paragraph(html_table(handicaps_after_this_game))


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

    generation = get_one_generation_from_gen_number(GET['gen'].value)
    if not generation:
        print "I can't find that generation number. How did you get to this page?"
        return

    show_game_shared(generation['game info'])

    winning_scores = get_winning_scores(
        generation['game info']['team colours'],
        generation['game info']['handicaps before this game']
    )

    red_net_handicap = get_net_handicap(
        generation['game info']['team colours'],
        generation['game info']['handicaps before this game']
    )

    print paragraph(handicap_difference_string(red_net_handicap))

    if 'red score' in generation:
        tense = "ed"
    else:
        tense = "s"

    for team_colour in ['red', 'blue']:
        print (
            paragraph(
                "{} team need{} {} to win and {} for handicap to change.",
                'class={}_team'.format(team_colour)
            ).format(
                team_colour.capitalize(),
                tense,
                winning_scores['to win'][team_colour],
                winning_scores['to change'][team_colour]
            )
        )

    if 'red score' in generation:
        game_not_played(GET['gen'].value)
    else:
        show_result(
            generation['red score'],
            generation['handicaps after'],
            winning_scores,
            generation['time'],
            generation['game info'],
            red_net_handicap,
        )

    return

main()
