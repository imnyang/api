from datetime import datetime
from pytz import timezone, all_timezones


def now(where:str):
    try:
        time = datetime.now(timezone(where))
        print(time)
        return {
            "success": True,
            "timestamp": time,
            "all": time.strftime('%Y-%m-%d %H:%M:%S'),
            "time": {
                "year": time.strftime('%Y'),
                "month": time.strftime('%m'),
                "day": time.strftime('%d'),
                "hour": time.strftime('%H'),
                "minute": time.strftime('%M'),
                "second": time.strftime('%S'),
            },
        }
    except:
        return {
            "success": False,
            "times": all_timezones
        }
