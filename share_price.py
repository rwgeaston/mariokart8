from datetime import datetime

from yahoo_finance import Share

csco = Share('CSCO')

def yesterdays_price_from_timestamp(timestamp):
    # there are things like bank holidays and weekends
    # i'm gonna be lazy and get the last several days
    # then use the data from the last of those
    # it might only return me one day
    # also any exception in this function needs to be non-fatal
    # can't risk breaking real functionality
    try:
        end = datetime.fromtimestamp(timestamp - 24 * 3600).strftime("%Y-%m-%d")
        start = datetime.fromtimestamp(timestamp - 5 * 24 * 3600).strftime("%Y-%m-%d")
        recent = csco.get_historical(start, end)
        yesterday_close = float(recent[0]['Close'])
        day_before_close = float(recent[1]['Close'])
        return yesterday_close - day_before_close
    except:
        return "Unknown"
