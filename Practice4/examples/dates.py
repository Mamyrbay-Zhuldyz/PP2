#Example 1
from datetime import date, datetime, time

today = date.today()
now = datetime.now()
current_time = time(14, 30, 45)

#Example 2
from datetime import datetime

now = datetime.now()
formatted1 = now.strftime("%Y-%m-%d")
formatted2 = now.strftime("%d.%m.%Y")
formatted3 = now.strftime("%H:%M:%S")

#Example 3
from datetime import date, timedelta

date1 = date(2024, 1, 1)
date2 = date(2024, 12, 31)
difference = date2 - date1

#Example 4
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(weeks=1)

#Example 5
from datetime import datetime

date_string = "2024-12-25"
date_object = datetime.strptime(date_string, "%Y-%m-%d")