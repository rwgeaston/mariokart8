def recent_players(game_count=50):
    with open("generation_log.txt") as generation_log_file:
        generation_log_raw = generation_log_file.readlines()

    generation_log_raw.reverse()

    all_recent_players = set()

    for game_raw in generation_log_raw[:game_count]:
        gen_number, game_info = eval(game_raw)
        all_recent_players.update(set(game_info['players']))

    return all_recent_players

def not_recent_players(game_count=50):
    with open('players.txt') as players_file:
        players_raw = players_file.readlines()

    all_players = set([line.split(',')[0] for line in players_raw])
    not_recent_players = all_players - recent_players(game_count)

    return not_recent_players
