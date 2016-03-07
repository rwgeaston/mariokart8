from time import time


def get_generations(count='all', reverse_order=True, start_point=0):
    """Get a range of generation logs

       Specify a start_point to get a particular range of generations.
       By default you get most recent games not oldest games."""

    if count == 'all':
        finish_point = -1
    else:
        finish_point = start_point + count

    with open("generation_log.txt") as generation_log_file:
        generation_log_raw = generation_log_file.readlines()

    if reverse_order:
        generation_log_raw.reverse()

    generations = []
    for generation in generation_log_raw[start_point:finish_point]:
        gen_number, game_info = eval(generation)
        generations.append(
            {'generation number': gen_number, 'game info': game_info}
        )

    return generations


def get_generations_with_results(count='all', reverse_order=True, start_point=0):
    """Get a range of generation logs with the associated results"""

    generations = get_generations(count, reverse_order, start_point)

    results = {}
    with open('results_log.txt') as results_log:
        for line in results_log.readlines():
            values = eval(line)
            if len(values) == 6:
                ian_watched = values[-1]
                values = values[:-1]
            else:
                ian_watched = False
            result_gen_number, red_score, players, handicaps_after, submit_time = values
            results[result_gen_number] = {
                "red score": red_score,
                "handicaps after": handicaps_after,
                "submit time": submit_time,
                "ian watched": ian_watched
            }

    for generation in generations:
        if generation['generation number'] in results:
            generation.update(results[generation['generation number']])

    return generations


def get_completed_generations_with_results(count='all', reverse_order=True, start_point=0):
    """Get a range of generation logs with the associated results"""
    if count == 'all':
        count = -1

    generations = get_generations_with_results('all', reverse_order, start_point)

    completed_generations = []

    for generation in generations:
        if 'red score' in generation:
            completed_generations.append(generation)

    return completed_generations[:count]


def get_one_generation_from_gen_number(gen_number):
    for generation in get_generations_with_results('all'):
        if generation['generation number'] == gen_number:
            return generation
    else:
        return None


def get_next_generation_number():
    try:
        last_generation = get_generations(1)[0]
    except IndexError:
        # wow, first ever game
        return 1
    else:
        return last_generation['generation number'] + 1


def append_result(gen_number, red_score, ian_watched, players, handicaps):
    with open('results_log.txt', 'a') as results_log:
        results_log.write(
            "{},{},{},{},{},{}\n"
            .format(gen_number, red_score, players, handicaps, time(), ian_watched)
        )


def append_generation(game_info):
    game_info['time'] = time()
    generation_number = get_next_generation_number()
    with open('generation_log.txt', 'a') as generation_log:
        generation_log.write('{},{}\n'.format(generation_number, game_info))
    return generation_number


def save_handicaps(handicaps):
    sorted_handicaps = sorted(handicaps, key=lambda person: -person[1])
    with open('players.txt', 'w') as handicap_file:
        for person in sorted_handicaps:
            handicap_file.write("{},{}\n".format(*person))


def get_current_handicaps():
    """Get the current handicaps from the players file."""
    handicaps = []
    with open('players.txt') as current_handicaps:
        for line in current_handicaps:
            player, handicap = line.strip().split(',')
            handicaps.append([player, float(handicap)])

    return handicaps
