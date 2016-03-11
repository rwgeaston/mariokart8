from mario_kart_files import get_generations_with_results
from share_price import yesterdays_price_from_timestamp

all_games = get_generations_with_results(reverse_order=False)

with open('share_prices.txt', 'a') as share_price_file:
    for game in all_games:
        if 'submit time' in game:
            share_price_file.write(
                '{}, {}\n'.format(
                    game['generation number'], 
                    yesterdays_price_from_timestamp(game['submit time'])
                )
            )
