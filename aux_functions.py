import DB.CRUD_DQL as crud_dql
from ERROR_files.CustomError import *
import numpy as np

"""This function pick up a list, takes the inner part of every subinterval out, letting just the edges of each subinterval.
Such new list will be returned
Ex.: input: [1, 2, 3, 6, 7, 8, 9, 110, 111, 112] ---> output: [1, 3, 6, 9, 110, 112]
"""
def let_just_the_extreme(list_of_distinct_numbers):

    def ascending_list(lst):
        for i in range(1, len(lst)):
            if lst[i-1] > lst[i]:
                return False
        return True

    def distinct_list(lst):
        for i in range(len(lst)):
            for j in range(len(lst)):
                if i != j and lst[i] == lst[j]:
                    return False
        return True
    
    if not distinct_list(list_of_distinct_numbers):
        raise NotDistinctError(list_of_distinct_numbers)
    
    if not ascending_list(list_of_distinct_numbers):
        raise NotAscendingError(list_of_distinct_numbers)
    
    aux_list = list()
    for i in range(len(list_of_distinct_numbers)):
        if i + 2 < len(list_of_distinct_numbers):
            if list_of_distinct_numbers[i + 1] == list_of_distinct_numbers[i] + 1 and list_of_distinct_numbers[i + 2] == list_of_distinct_numbers[i + 1] + 1:
                aux_list.append(list_of_distinct_numbers[i + 1])
    for data in aux_list:
        list_of_distinct_numbers.remove(data)
    return list_of_distinct_numbers

def transform_date(date_str):
    
    def check_date(date_str):
        if date_str[4] == '-' and date_str[7] == '-' and len(date_str) == 10:
            return date_str
        raise InvalidDateError(date_str)
    
    def check_range_val(num):
        if num not in range(1, 13):
            raise RangeError(1, 12)
        return num

    def transform_month(num):
        match num:
            case 1:
                return 'jan'
            case 2:
                return 'feb'
            case 3:
                return 'mar'
            case 4:
                return 'april'
            case 5:
                return 'may'
            case 6:
                return 'june'
            case 7:
                return 'july'
            case 8:
                return 'aug'
            case 9:
                return 'sep'
            case 10:
                return 'oct'
            case 11:
                return 'nov'
            case 12:
                return 'dec'
    if not isinstance(date_str, str):
        raise TypeError(f'Transform_date() function takes date_str argument as str, not {type(date_str)}')
    try:
        date_str = check_date(date_str)
    except InvalidDateError as e:
        print(e)
        print(e.describe())
    else:
        date_pieces = date_str.split('-')
        try:
            day = str(int(date_pieces[2]))
            if len(day) == 1:
                day = '0' + day
            new_format_date = day + ', ' + transform_month(check_range_val(int(date_pieces[1])))
        except RangeError as e:
            print(e)
            print(e.describe())
        else:
            return new_format_date

def get_temp_danger_info(db):
    high_temp_dataset = crud_dql.danger_time_temp(db, 0)
    low_temp_dataset = crud_dql.danger_time_temp(db, 1)
    info_high_temp = "High Temperature info:\n\n"
    if len(high_temp_dataset) != 0:
        for data in high_temp_dataset:
            info_high_temp += f"Date >> {data['day']} {data['time']}\nTemperature >> {data['temperature']}°C\n\n"
    else:
        info_high_temp += 'No high temperature for the next 3 days\n'
    info_low_temp = "Low temperature info:\n\n"
    if len(low_temp_dataset) != 0:
        for data in low_temp_dataset:
            info_low_temp += f"Date >> {data['day']} {data['time']}\nTemperature >> {data['temperature']}°C\n\n"
    else:
        info_low_temp += 'No low temperature for the next 3 days\n'
    return info_low_temp, info_high_temp

def get_extreme_temp_per_day(db):
    info_str = 'Extreme temperatures\n\n'
    dataset = crud_dql.min_max_temp(db)
    for data in dataset:
        info_str += f'Day {transform_date(data['day'])}\nMinimum >> {data['min_temp']}°C\nMaximum >> {data['max_temp']}°C\n\n'
    return info_str

def get_hum_danger_info(db):
    high_hum = crud_dql.danger_time_humidity(db, 0)
    low_hum = crud_dql.danger_time_humidity(db, 1)
    info_high_hum = 'High humidity info:\n\n'
    if len(high_hum) > 0:
        for data in high_hum:
            info_high_hum += f"Date >> {data['day']} {data['time']}\nHumidity >> {data['humidity']}%\n\n"
    else:
        info_high_hum += 'No high humidity for the next 3 days\n\n'
    info_low_hum = 'Low humidity info:\n\n'
    if len(low_hum) > 0:
        for data in low_hum:
            info_low_hum += f"Date >> {data['day']} {data['time']}\nHumidity >> {data['humidity']}%\n\n"
    else:
        info_low_hum += 'No low humidity for the next 3 days\n\n'
    return info_low_hum, info_high_hum

def get_extremes_per_day_hum(db):
    info_str = 'Extreme humidity\n\n'
    dataset = crud_dql.min_max_humidity(db)
    for data in dataset:
        info_str += f'Day {transform_date(data['day'])}\nMinimum >> {data['min_humidity']}%\nMaximum >> {data['max_humidity']}%\n\n'
    return info_str

def get_rain_data_organized(db):
    info_str = 'Precipitation data for the next 3 days:\n\n'
    everything = crud_dql.all_data(db)
    days = np.array_split(np.array(everything), 3)
    days_data = crud_dql.evaluate_avg_over_group(db)
    days_names = [transform_date(days_data[i]['date']) for i in range(3)]
    for day in range(3):
        info_str += f'Day {days_names[day]} data:\n'
        for hour in range(24):
            if hour < 12:
                if len(str(hour)) == 1:
                    info_str += f'  Hour: {hour}AM '
                else:
                    info_str += f'  Hour: {hour}AM'
            else:
                if len(str(hour - 12)) == 1:
                    info_str += f'  Hour: {hour - 12}PM '
                else:
                    info_str += f'  Hour: {hour - 12}PM'
            info_str += f'  |   amount: {days[day][hour]['precipitation']}mm\n'
        info_str += '\n\n'
    return info_str

'''This function takes a full datetime and returns the same data in a beautiful way.
Ex.: 2025-26-10 18:24:30 ---> 26, oct 06:25:30 PM'''
def beaulty_date(datetime):
    if not isinstance(datetime, str):
        raise TypeError(f"beaulty_date() function's parameter takes str as argument, not {type(datetime)}")
    if not (len(datetime) == 19 and datetime[4] == '-' and datetime[7] == '-' and datetime[10] == ' ' and datetime[13] == ':' and datetime[16] == ':'):
        raise InvalidDateTimeError(datetime)
    pieces = datetime.split()
    only_date = pieces[0]
    only_time = pieces[1]
    treated_time = ''
    if int(only_time[0:2]) < 12:
        treated_time += only_time + ' AM'
    else:
        hour_str = only_time[:2]
        hour_int = int(hour_str)
        if len(str(hour_int - 12)) == 1:
            new_hour_str = '0' + str(hour_int - 12)
        else:
            new_hour_str = str(hour_int - 12)
        for i in range(len(only_time)):
            if i in range(0, 2):
                treated_time += new_hour_str[i]
            else:
                treated_time += only_time[i]
        treated_time += ' PM'
    treated_date = transform_date(only_date)
    full_date = treated_date + ' ' + treated_time
    return full_date

if __name__ == '__main__':
    pass