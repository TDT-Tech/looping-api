import datetime

from dateutil.relativedelta import relativedelta


def calculate_next_issue_date(schedule, last_issue_date):
    if schedule == "BIWEEKLY":
        next_issue_date = last_issue_date + datetime.timedelta(days=14)
    elif schedule == "QUARTERLY":
        next_issue_date = last_issue_date + relativedelta(months=+3)
    else:
        next_issue_date = last_issue_date + relativedelta(months=+1)

    return next_issue_date
