import pandas as pd
import os
import DB.CRUD_DDL as crud_ddl
import DB.CRUD_DQL as crud_dql
from ERROR_files import CustomError as err
import aux_functions

def create_csv_dir():
    if not os.path.exists('CSV_files'):
        os.mkdir('CSV_files')
        os.mkdir('CSV_files/temperature')
        os.mkdir('CSV_files/humidity')
        os.mkdir('CSV_files/rain')

def alldata_csv_gen(db):
    dataset = crud_dql.all_data(db)
    data = {'city': [record['city name'] for record in dataset],
            'country': [record['country'] for record in dataset],
            'temperature (°C)': [record['temperature'] for record in dataset],
            'will it rain': [str(record['will it rain']) for record in dataset],
            'will it snow': [str(record['will it snow']) for record in dataset],
            'forecast date': [aux_functions.beaulty_date(record['forecast date']) for record in dataset],
            'humidity (%)': [record['humidity'] for record in dataset],
            'precipitation (mm)': [record['precipitation'] for record in dataset],
            'rain prob (%)': [record['rain prob'] for record in dataset],
            'snow prob (%)': [record['snow prob'] for record in dataset]}
    df = pd.DataFrame(data)
    df.dropna(inplace  = True) #Cleaning NaN or NaT data.
    for ind in df.index: #Replacing not-cool data to friendly data inside the dataframe that will be exported as CSV file.
        if df.loc[ind, 'will it rain'] == '1':
            df.loc[ind, 'will it rain'] = 'Yes'
        else:
            df.loc[ind, 'will it rain'] = 'No'
        if df.loc[ind, 'will it snow'] == '1':
            df.loc[ind, 'will it snow'] = 'Yes'
        else:
            df.loc[ind, 'will it snow'] = 'No'
    if os.path.exists('CSV_files'):
        df.to_csv('CSV_files/everything.csv', index = False)
    else:
        raise err.NotFoundDir('CSV_files')

def average_data_csv_gen(db):
    dataset = crud_dql.evaluate_avg_over_group(db)
    data = {
        'Date': [aux_functions.transform_date(record['date']) for record in dataset],
        'Average Temperature (°C)': [record['avg_temp'] for record in dataset],
        'Average Humidity (%)': [record['avg_humidity'] for record in dataset]
    }
    df = pd.DataFrame(data)
    df.dropna(inplace = True) #Cleaning NaN or NaT values.
    if os.path.exists('CSV_files'):
        df.to_csv('CSV_files/averages.csv', index = False)
    else:
        raise err.NotFoundDir('CSV_files')

def min_max_temp_csv_gen(db):
    dataset = crud_dql.min_max_temp(db)
    data = {
        'Day': [aux_functions.transform_date(record['day']) for record in dataset],
        'Max Temperature (°C)': [record['max_temp'] for record in dataset],
        'Min Temperature (°C)': [record['min_temp'] for record in dataset]
    }
    df = pd.DataFrame(data)
    df.fillna('Undefined', inplace = True) #Substitute Nan, None and NaT by 'Undefined' if necessary
    if os.path.exists('CSV_files/temperature'):
        df.to_csv('CSV_files/temperature/min_max_temp.csv', index = False)
    else:
        raise err.NotFoundDir('CSV_files/temperature')

def danger_temp_csv_gen(db, mode): #0 for high temperature, 1 for low temperature
    if mode not in (0, 1):
        raise err.RangeError(0, 1)
    if not isinstance(mode, int):
        raise TypeError(f'The value must be a binary, 0 or 1, not {mode}')
    match mode:
        case 0:
            dataset = crud_dql.danger_time_temp(db, 0) #Querying high temperatures
            if len(dataset) > 0:
                data = {
                    'Date': [aux_functions.beaulty_date(record['day'] + ' ' + str(record['time'])) for record in dataset],
                    'Temperature (°C)': [record['temperature'] for record in dataset]
                }
            else:
                data = {'There is not a high temperature (greater than 32°C)': [None]}
            df = pd.DataFrame(data)
            df.dropna(inplace = True)
            if os.path.exists('CSV_files/temperature'):
                df.to_csv('CSV_files/temperature/danger_HIGH_temp.csv', index = False)
            else:
                raise err.NotFoundDir('CSV_files/temperature')
        case 1:
            dataset = crud_dql.danger_time_temp(db, 1) #Querying low temperatures
            if len(dataset) > 0:
                data = {
                    'Date': [record['day'] + ' ' + str(record['time']) for record in dataset],
                    'Temperature (°C)': [record['temperature'] for record in dataset]
                }
            else:
                data = {'There is not a low temperature (lower than 12°C)': [None]}
            df = pd.DataFrame(data)
            df.dropna(inplace = True)
            if os.path.exists('CSV_files/temperature'):
                df.to_csv('CSV_files/temperature/danger_LOW_temp.csv', index = False)
            else:
                raise err.NotFoundDir('CSV_files/temperature')

def min_max_humidity_csv_gen(db):
    dataset = crud_dql.min_max_humidity(db)
    data = {
        'Day': [aux_functions.transform_date(record['day']) for record in dataset],
        'Min Humidity (%)': [record['min_humidity'] for record in dataset],
        'Max Humidity (%)': [record['max_humidity'] for record in dataset]
    }
    df = pd.DataFrame(data)
    df.dropna(inplace = True)
    if os.path.exists('CSV_files/humidity'):
        df.to_csv('CSV_files/humidity/min_max_humidity.csv', index = False)
    else:
        raise err.NotFoundDir('CSV_files/humidity')

def danger_humidity_csv_gen(db, mode): #0 for high humidity, 1 for low humidity
    if mode not in (0, 1):
        raise err.RangeError(0, 1)
    if not isinstance(mode, int):
        raise TypeError(f'The value must be a binary, 0 or 1, not {mode}')
    match mode:
        case 0:
            dataset = crud_dql.danger_time_humidity(db, 0) #Querying high humidity
            if len(dataset) > 0:
                data = {
                    'Date': [record['day'] + ' ' + str(record['time']) for record in dataset],
                    'Humidity (%)': [record['humidity'] for record in dataset]
                }
            else:
                data = {'There is not a high humidity (greater than 80%)': [None]}
            df = pd.DataFrame(data)
            df.dropna(inplace = True)
            if os.path.exists('CSV_files/humidity'):
                df.to_csv('CSV_files/humidity/danger_HIGH_humidity.csv', index = False)
            else:
                raise err.NotFoundDir('CSV_files/humidity')
        case 1:
            dataset = crud_dql.danger_time_humidity(db, 1) #Querying low humidity
            if len(dataset) > 0:
                data = {
                    'Date': [record['day'] + ' ' + str(record['time']) for record in dataset],
                    'Humidity (%)': [record['humidity'] for record in dataset]
                }
            else:
                data = {'There is not a low humidity (lower than 20%)': [None]}
            df = pd.DataFrame(data)
            df.dropna(inplace = True)
            if os.path.exists('CSV_files/humidity'):
                df.to_csv('CSV_files/humidity/danger_LOW_humidity.csv', index = False)
            else:
                raise err.NotFoundDir('CSV_files/humidity')

def rain_day_info_csv_gen(db):
    dataset = crud_dql.get_precipt_info(db)
    data = {
        'day': [record['day'] for record in dataset],
        'precipitation (mm)': [record['preciptation_mm'] for record in dataset],
        'classification': [record['rain class'] for record in dataset]
    }
    df = pd.DataFrame(data)
    df.fillna('Undefined', inplace = True)
    if os.path.exists('CSV_files/rain'):
        df.to_csv('CSV_files/rain/rain_info_by_day.csv', index = False)
    else:
        raise err.NotFoundDir('CSV_files/rain')

def remove_csv_dir():
    if os.path.exists('CSV_files'):
        if os.path.exists('CSV_files/averages.csv'):
            os.remove('CSV_files/averages.csv')
        if os.path.exists('CSV_files/everything.csv'):
            os.remove('CSV_files/everything.csv')
        if os.path.exists('CSV_files/humidity'):
            if os.path.exists('CSV_files/humidity/danger_LOW_humidity.csv'):
                os.remove('CSV_files/humidity/danger_LOW_humidity.csv')
            if os.path.exists('CSV_files/humidity/danger_HIGH_humidity.csv'):
                os.remove('CSV_files/humidity/danger_HIGH_humidity.csv')
            if os.path.exists('CSV_files/humidity/min_max_humidity.csv'):
                os.remove('CSV_files/humidity/min_max_humidity.csv')
            os.rmdir('CSV_files/humidity')
        if os.path.exists('CSV_files/temperature'):
            if os.path.exists('CSV_files/temperature/danger_HIGH_temp.csv'):
                os.remove('CSV_files/temperature/danger_HIGH_temp.csv')
            if os.path.exists('CSV_files/temperature/danger_LOW_temp.csv'):
                os.remove('CSV_files/temperature/danger_LOW_temp.csv')
            if os.path.exists('CSV_files/temperature/min_max_temp.csv'):
                os.remove('CSV_files/temperature/min_max_temp.csv')
            os.rmdir('CSV_files/temperature')
        if os.path.exists('CSV_files/rain'):
            if os.path.exists('CSV_files/rain/rain_info_by_day.csv'):
                os.remove('CSV_files/rain/rain_info_by_day.csv')
            os.rmdir('CSV_files/rain')
        os.rmdir('CSV_files')

def generate_csv_files(db): #This function will use all the others at once. It will create the directories and CSV files at each directory.
    try:
        remove_csv_dir() #Remove directories and previous CSV files
        create_csv_dir() #Recreate directories and CSV files
    except Exception as ERROR:
        print(ERROR)
        print('Did you change the directory CSV_files? Try to delete this folder and restart the app.')
    else:
        try:
            alldata_csv_gen(db)
            average_data_csv_gen(db)
            min_max_temp_csv_gen(db)
            danger_temp_csv_gen(db, 0)
            danger_temp_csv_gen(db, 1)
            min_max_humidity_csv_gen(db)
            danger_humidity_csv_gen(db, 0)
            danger_humidity_csv_gen(db, 1)
            rain_day_info_csv_gen(db)
        except err.NotFoundDir as ERROR:
            print(ERROR)

if __name__ == '__main__':
    remove_csv_dir()