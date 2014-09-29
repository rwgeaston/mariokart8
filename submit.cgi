#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgitb
from cgi import FieldStorage
from show_game_shared_code import get_winning_scores
from decay import not_recent_players
from mario_kart_files import get_current_handicaps, get_one_generation_from_gen_number, \
    save_handicaps, append_result

#enable debugging
cgitb.enable()
GET = FieldStorage()

print "Content-Type: text/html"
print

print '''
<html>
<head>
<title>MK8: Submit result</title>
</head>
'''


def invalid_score(message):
    print message.replace('\n', '<br />')
    print ('<br><a href="show_generation.cgi?gen={}">'
           'Return to team generation page.</a>'
           .format(GET['gen'].value))
    return


def handicap_change(selection, change_direction):
    handicaps = get_current_handicaps()

    for player, team in zip(selection['players'], selection['team colours']):
        for person in handicaps:
            if player == person[0]:
                if team == 'red':
                    person[1] += 0.25 * change_direction
                else:
                    person[1] -= 0.25 * change_direction

    # Find AI handicap to set it back to 0
    for person in handicaps:
        if person[0] == 'Computer':
            computer_handicap = person[1]
            break
    else:
        raise Exception("Why isn't the computer in the handicaps list?")

    for person in handicaps:
        person[1] -= computer_handicap

    save_handicaps(handicaps)


def decay_handicaps():
    handicaps = get_handicaps()
    players_to_decay = not_recent_players()

    for player in handicaps:
        if player[0] in players_to_decay and player[1] > 0:
            player[1] -= 0.25

    save_handicaps(handicaps)


def main():
    for key in ['gen', 'redscore']:
        if key not in GET:
            print "You don't have a {} value in the GET. How did you get to this page?".format(key)
            return

    generation = get_one_generation_from_gen_number(int(GET['gen'].value))
    if not generation:
        print "I can't find that generation number. How did you get to this page?"
        return

    try:
        red_score = int(GET['redscore'].value)
    except ValueError:
        return invalid_score("I don't think you submitted an integer for the red team score.")

    if red_score < 105 or red_score > 305:
        return invalid_score("One of us doesn't know how mario kart scoring works.")

    scores_to_win = get_winning_scores(
        generation['game info']['team colours'],
        generation['game info']['handicaps before this game'])

    if red_score >= scores_to_win['to change']['red']:
        handicap_change(generation['game info'], 1)
    elif (410 - red_score) >= scores_to_win['to change']['blue']:
        handicap_change(generation['game info'], -1)

    if generation['generation number'] % 10 == 0:
        decay_handicaps()

    handicaps = get_current_handicaps()

    append_result(
        generation['generation number'],
        red_score,
        generation['game info']['players'],
        handicaps
    )

    return

main()

print '''
<html>
<head>
<title>Show random team generation</title>
<meta http-equiv="refresh" content="1;url=show_game.cgi?gen={gen_num}">
    <script type="text/javascript">
        window.location.href = "show_game.cgi?gen={gen_num}"
    </script>
    <title>Page Redirection</title>
</head>
<body>
    If you are not redirected automatically, please click to see
    <a href="show_game.cgi?gen={gen_num}"> generation log</a>
</body>
</html>'''.format(gen_num=GET['gen'].value)
