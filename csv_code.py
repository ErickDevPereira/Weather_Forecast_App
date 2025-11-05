import pandas as pd
import os
import DB.CRUD_DDL as crud_ddl
import DB.CRUD_DQL as crud_dql
import ERROR_files.CustomError as err
import aux_functions

def create_csv_dir():
    if not os.path.exists('CSV_files'):
        os.mkdir('CSV_files')
        os.mkdir('CSV_files/temperature')
        os.mkdir('CSV_files/humidity')
        os.mkdir('CSV_files/snow_rain')

def alldata_csv_gen():
    db = crud_ddl.define_conn('root', 'Ichigo007*')
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

if __name__ == '__main__':
    os.rmdir('CSV_files/humidity')
    os.rmdir('CSV_files/snow_rain')
    os.rmdir('CSV_files/temperature')
    os.rmdir('CSV_files')
    create_csv_dir()
    alldata_csv_gen()