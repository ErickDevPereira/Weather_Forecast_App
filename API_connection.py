import requests
import DB.CRUD_DML as crud_dml
import time

'''Creating a decorator that returns the execution time of the API_to_DB function.
It is made based on the API_to_DB function, but it can be used on some other functions as well'''
def get_exe_time(func):

    def wrapper(*args, **kwargs):
        initial_time = time.time()
        signal, status_code = func(*args, **kwargs)
        final_time = time.time()
        tot_time = f'{final_time - initial_time:.2f} sec'
        return signal, status_code, tot_time
    
    return wrapper

#This function returns 0 if we can't achieve data for such city, 1 if it can reach data for such city
def check_if_connection_is_set(city_name, *, url, token):

    api_URL = url
    parameters = {'key' : token, 'q' : city_name}
    response = requests.get(api_URL, params = parameters)
    if response.status_code == 200:
        return 1
    else:
        return 0

@get_exe_time
def API_to_DB(database_conn, city_name, *, url, token):
    URL = url
    parameters = {'key' : token, 'q' : city_name, 'days' : 7}

    response = requests.get(URL, params = parameters)
    status_code = response.status_code
    if status_code == 200:
        data_structure = response.json()
        country = data_structure['location']['country']
        crud_dml.charge_DB(database_conn,
                               mode = 1,
                               city_id = 1,
                               city_name = city_name,
                               country = country,
                               temperature = None,
                               will_it_rain = None,
                               will_it_snow = None,
                               forecast_date = None,
                               humidity = None,
                               precipitation = None,
                               prob_id = None,
                               rain_prob = None,
                               snow_prob = None,
                               cur_temp = None,
                               cur_ws = None,
                               cur_hum = None,
                               cur_is_day = None,
                               cur_last_update = None,
                               cur_cloud = None
                               ) #Inserting data into city_data
        prob_id = 0 #Declaring the id variable that will insert ids inside probabilities in a FK column that references PK id column from weather_data table.
        for day in range(3):
            day_data = data_structure['forecast']['forecastday'][day]['hour']
            for hour in range(24):
                prob_id += 1
                temperature = day_data[hour]['temp_c']
                will_it_rain = day_data[hour]['will_it_rain']
                will_it_snow = day_data[hour]['will_it_snow']
                forecast_data = ':'.join([day_data[hour]['time'], '00'])
                humidity = day_data[hour]['humidity']
                precipitation = day_data[hour]['precip_mm']
                crud_dml.charge_DB(database_conn,
                               mode = 0,
                               city_id = 1,
                               city_name = None,
                               country = None,
                               temperature = temperature,
                               will_it_rain = will_it_rain,
                               will_it_snow = will_it_snow,
                               forecast_date = forecast_data,
                               humidity = humidity,
                               precipitation = precipitation,
                               prob_id = None,
                               rain_prob = None,
                               snow_prob = None,
                               cur_temp = None,
                               cur_ws = None,
                               cur_hum = None,
                               cur_is_day = None,
                               cur_last_update = None,
                               cur_cloud = None
                                ) #Inserting row at Weather_data table
                rain_prob = day_data[hour]['chance_of_rain']
                snow_prob = day_data[hour]['chance_of_snow']
                crud_dml.charge_DB(database_conn,
                                mode = -1,
                                city_id = 1,
                                city_name = None,
                                country = None,
                                temperature = None,
                                will_it_rain = None,
                                will_it_snow = None,
                                forecast_date = None,
                                humidity = None,
                                precipitation = None,
                                prob_id = prob_id,
                                rain_prob = rain_prob,
                                snow_prob = snow_prob,
                                cur_temp = None,
                                cur_ws = None,
                                cur_hum = None,
                                cur_is_day = None,
                                cur_last_update = None,
                                cur_cloud = None
                                ) #Inserting row at probabilities table
        cur_temp = data_structure['current']['temp_c']
        cur_ws = data_structure['current']['wind_kph']
        cur_hum = data_structure['current']['humidity']
        cur_is_day = data_structure['current']['is_day']
        cur_last_update = data_structure['current']['last_updated']
        cur_cloud = data_structure['current']['cloud']
        crud_dml.charge_DB(database_conn,
                                city_id = None,
                                city_name = None,
                                country = None,
                                temperature = None,
                                will_it_rain = None,
                                will_it_snow = None,
                                forecast_date = None,
                                humidity = None,
                                precipitation = None,
                                prob_id = None,
                                rain_prob = None,
                                snow_prob = None,
                                cur_temp = cur_temp,
                                cur_ws = cur_ws,
                                cur_hum = cur_hum,
                                cur_is_day = cur_is_day,
                                cur_last_update = cur_last_update,
                                cur_cloud = cur_cloud
                                )
        return 1, status_code #Case at which the connection to API is ok
    else:
        return 0, status_code #Bad scenario: a connection error happened along the way