from datetime import datetime, timedelta


def time_checker(talks, my_name, your_name):
    me = []
    you = []

    talks = sorted(talks, key=lambda x : x.date)
    for i in range(len(talks)-1):
        talk1, talk2 = talks[i], talks[i+1]
        if talk1.date == 'Invalid Date' or talk2.date == 'Invalid Date': continue 
        date1 = datetime.strptime(talk1.date, "%a, %d %b %Y %H:%M:%S %Z")
        date2 = datetime.strptime(talk2.date, "%a, %d %b %Y %H:%M:%S %Z")

        time_difference = max(date1, date2) - min(date1, date2)
        print()
        print(time_difference)
        if talk1.sender != talk2.sender:
            if talk1.sender == my_name and talk2.sender == your_name: you.append(time_difference)
            else: me.append(time_difference)
        print()
    print(me)
    print()
    print(you)
    print()
    me_sum = 0
    if len(me) > 1:
        me_sum = sum(((date - me[0]) for date in me[1:]), timedelta())
    else:
        me_sum = me[0]
    
    you_sum = 0
    if len(you) > 1:
        you_sum = sum(((date - you[0]) for date in you[1:]), timedelta())
    else:
        you_sum = timedelta()

    print("????????????????????????")
    print(me_sum)
    print("///////////////////////")
    print(you_sum)
    print("????????????????????????")

    return {"my_reply_time": me_sum, "you_reply_time": you_sum}