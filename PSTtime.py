from datetime import datetime, timedelta
from pytz import timezone
import pytz


# return data received time in Pacific Time (PST)
def pst_date(days, hours, minutes, seconds):
    date_format = '%A %m/%d/%Y %I:%M %p %Z'
    # current time - posted ago time
    date = datetime.now(tz=pytz.utc) - timedelta(days=days,
                                                 hours=hours, minutes=minutes, seconds=seconds)
    # print('Current date & time is:', date.strftime(date_format))
    date = date.astimezone(timezone('US/Pacific'))
    pst_date = date.strftime(date_format)
    # print('Local date & time is  : {}'.format(pst_date))
    return pst_date
