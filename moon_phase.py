from astral import Astral
from datetime import datetime

a = Astral()
city = a['London']

def moon_phase_number(timestamp):
    return city.moon_phase(datetime.fromtimestamp(timestamp))

# Stop when you get to a number >= than the one returned by moon_phase_number to get the current phase
phase_name_mapping = [
    ('new moon', 27),
    ('waning crescent', 21),
    ('waning gibbous', 16),
    ('full moon', 13),
    ('waxing gibbous', 8),
    ('waxing crescent', 2),
    ('new moon', 0)
]

def moon_phase_name(timestamp):
    phase_number = moon_phase_number(timestamp)
    for phase, start_day in phase_name_mapping:
        if phase_number >= start_day:
            return phase
    else:
        raise Exception("What moon phase is this supposed to be? {} {}".format(timestamp, phase_number))

