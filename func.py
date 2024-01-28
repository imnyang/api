from datetime import datetime
from pytz import timezone


def now(where:str):
    time = datetime.now(timezone(where))

    return {
        "success": True,
        "timestamp": time,
        "all": time.strftime('%Y-%m-%d %H:%M:%S'),
        "year": time.strftime('%Y'),
        "month": time.strftime('%m'),
        "day": time.strftime('%d'),
        "hour": time.strftime('%H'),
        "minute": time.strftime('%M'),
        "second": time.strftime('%S'),
    }
