import shelve


def double_return():
    with shelve.open('time_to_run') as tr:
        hour = tr.get('clock')
        new_hour = hour.split(':')[0] + ':' + str(int(hour.split(':')[1]) + 1)
        return hour, new_hour


print(double_return()[1])
