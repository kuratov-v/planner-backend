from datetime import datetime, timedelta


def get_week_range(year, week):
    """ Return first day and last day of week by year and week number """
    first_day = datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w").date()
    last_day = first_day + timedelta(days=6)
    return first_day, last_day
