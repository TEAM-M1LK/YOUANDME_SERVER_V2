from datetime import datetime, timedelta
from pydantic import BaseModel

def time_checker(talks, me, you):
    me = []
    you = []

    talks = sorted(talks, key=lambda x : x.date)
    for i in range(len(talks)-1):
        talk1, talk2 = talks[i], talks[i+1]
        date1 = datetime.strptime(talk1.date, "%a, %d %b %Y %H:%M:%S %Z")
        date2 = datetime.strptime(talk2.date, "%a, %d %b %Y %H:%M:%S %Z")

        time_difference = max(date1, date2) - min(date1, date2)
        print()
        print(time_difference)
        if talk1.sender != talk2.sender:
            if talk1.sender == "우빈" and talk2.sender == "유정": you.append(time_difference)
            else: me.append(time_difference)
        print()
    print(me)
    print()
    print(you)
    print()
    me_sum = sum(((date - me[0]) for date in me[1:]), timedelta())
    you_sum = sum(((date - you[0]) for date in you[1:]), timedelta())
    print(me_sum)
    print(you_sum)