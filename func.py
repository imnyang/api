from datetime import datetime
from pytz import timezone


def kst_now():
    all = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    year = datetime.now(timezone('Asia/Seoul')).strftime('%Y')
    month = datetime.now(timezone('Asia/Seoul')).strftime('%m')
    day = datetime.now(timezone('Asia/Seoul')).strftime('%d')
    hour = datetime.now(timezone('Asia/Seoul')).strftime('%H')
    minute = datetime.now(timezone('Asia/Seoul')).strftime('%M')
    second = datetime.now(timezone('Asia/Seoul')).strftime('%S')
    return {
        "all": all,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
    }

