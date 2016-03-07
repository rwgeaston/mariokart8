from mario_kart_files import get_generations, get_current_handicaps


def recent_players(game_count=50):
    generations = get_generations(game_count)

    all_recent_players = set()
    for generation in generations:
        all_recent_players.update(set(generation['game info']['players']))

    return all_recent_players


def not_recent_players(game_count=50):
    all_players = set([player[0] for player in get_current_handicaps()])
    not_recent_players = all_players - recent_players(game_count)

    return not_recent_players
