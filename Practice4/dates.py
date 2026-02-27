from datetime import datetime, date, timedelta


def subtract_five_days_from_today():
    today = date.today()
    return today - timedelta(days=5)


def print_yesterday_today_tomorrow():
    today = date.today()
    y = today - timedelta(days=1)
    t = today + timedelta(days=1)
    return y, today, t


def drop_microseconds(dt: datetime):
    return dt.replace(microsecond=0)


def difference_in_seconds(dt1: datetime, dt2: datetime):
    delta = dt2 - dt1
    return int(delta.total_seconds())


if __name__ == "__main__":
    print(subtract_five_days_from_today())

    y, td, tm = print_yesterday_today_tomorrow()
    print(y)
    print(td)
    print(tm)
    s = input().strip()
    dt = datetime.fromisoformat(s)
    print(drop_microseconds(dt))

    s1 = input().strip()
    s2 = input().strip()
    dt1 = datetime.fromisoformat(s1)
    dt2 = datetime.fromisoformat(s2)
    print(difference_in_seconds(dt1, dt2))