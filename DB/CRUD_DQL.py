'''The following function will return a list of dictionaries, where each dictionary will store
data related to one of the next 3 days. The least will contain data for 3 days straight.'''

def evaluate_avg_over_group(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT 
                        DATE(forecast_date) AS date,
                        FORMAT(AVG(temperature), 2) AS avg_temp,
                        FORMAT(AVG(humidity), 2) AS avg_humidity
                    FROM 
                        weather_data
                    GROUP BY
                        DATE(forecast_date)
                """)
    result = cursor.fetchall() #Returning records as (date, avg_temp, avg_humidity)
    data_set = list()
    for record in result:
        data_set.append({'date' : str(record[0]),
                         'avg_temp' : float(record[1]),
                         'avg_humidity' : float(record[2])})
    cursor.close()
    return data_set

def days_that_will_rain(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        DATE(forecast_date) AS 'Rain day',
                        TIME(forecast_date) AS 'Rain hour',
                        temperature AS 'temperature (°C)',
                        humidity AS 'humidity (%)'
                    FROM
                        weather_data
                    WHERE
                        will_it_rain = 1
                    ORDER BY
                        forecast_date
                    """)
    results = cursor.fetchall()
    dataset = list()
    for record in results:
        dataset.append({
                        'rain day' : str(record[0]),
                        'rain hour' : record[1],
                        'temperature' : record[2],
                        'humidity' : record[3]
                        })
    cursor.close()
    return dataset

def days_that_will_snow(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        DATE(forecast_date) AS 'Snow day',
                        TIME(forecast_date) AS 'Snow hour',
                        temperature AS 'temperature (°C)',
                        humidity AS 'humidity (%)'
                    FROM
                        weather_data
                    WHERE
                        will_it_snow = 1
                    ORDER BY
                        forecast_date
                    """)
    results = cursor.fetchall()
    dataset = list()
    for record in results:
        dataset.append({
                        'snow day' : str(record[0]),
                        'snow hour' : record[1],
                        'temperature' : record[2],
                        'humidity' : record[3]
                        })
    cursor.close()
    return dataset

def all_data(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        cd.city_name AS city_name,
                        cd.country AS country,
                        wd.temperature AS temperature,
                        wd.will_it_rain,
                        wd.will_it_snow,
                        wd.forecast_date AS forecast_date,
                        wd.humidity AS humidity,
                        wd.precipitation AS precipitation,
                        pb.rain_prob AS rain_probability,
                        pb.snow_prob AS snow_probability
                    FROM 
                        city_data AS cd INNER JOIN
                        weather_data AS wd ON cd.city_id = wd.city_id
                        INNER JOIN probabilities AS pb ON pb.prob_id = wd.id
                    ORDER BY
                        wd.forecast_date
                    """)
    results = cursor.fetchall()
    dataset = list()
    for record in results:
        dataset.append({
                        'city name' : record[0],
                        'country' : record[1],
                        'temperature' : record[2],
                        'will it rain' : record[3],
                        'will it snow' : record[4],
                        'forecast date' : str(record[5]),
                        'humidity' : record[6],
                        'precipitation' : record[7],
                        'rain prob' : record[8],
                        'snow prob' : record[9]
                        })
    cursor.close()
    return dataset

#Mode = 1 returns the raining moments, mode = 0 returns the snowing moments
def rain_snow_data(db, mode):
    if mode == 1:
        cursor = db.cursor()
        cursor.execute('''
                        SELECT
                            DATE(forecast_date) AS raining_day,
                            HOUR(forecast_date) AS raining_hour
                        FROM
                            weather_data
                        WHERE
                            will_it_rain = 1
                        ORDER BY raining_day, raining_hour
                        ''')
        dataset = cursor.fetchall()
        cursor.close()
    if mode == 0:
        cursor = db.cursor()
        cursor.execute('''
                        SELECT
                            DATE(forecast_date) AS snowing_day,
                            HOUR(forecast_date) AS snowing_hour
                        FROM
                            weather_data
                        WHERE
                            will_it_snow = 1
                        ORDER BY snowing_day, snowing_hour
                        ''')
        dataset = cursor.fetchall()
        cursor.close()
    aux_dataset = evaluate_avg_over_group(db)
    day1, day2, day3 = aux_dataset[0]['date'], aux_dataset[1]['date'], aux_dataset[2]['date']
    hours1, hours2, hours3 = list(), list(), list()
    for data in dataset:
        if data[0] == day1:
            hours1.append(data[1])
        if data[0] == day2:
            hours2.append(data[1])
        if data[0] == day3:
            hours3.append(data[1])
    treated_dataset = {day1 : hours1, day2 : hours2, day3 : hours3}
    return treated_dataset #Returns a dictionary with the forecast day as key and list with hours of raining/snowing as value

def min_max_temp(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        MIN(temperature) AS min_temp,
                        MAX(temperature) AS max_temp,
                        DATE(forecast_date) AS day
                    FROM
                        weather_data
                    GROUP BY
                        day
                    ORDER BY day
                    """)
    dataset = cursor.fetchall()
    cursor.close()
    organized_data = []
    for data in dataset:
        organized_data.append({'day' : str(data[2]), 'min_temp' : data[0], 'max_temp' : data[1]})
    return organized_data

def min_max_humidity(db):
    cursor = db.cursor()
    cursor.execute('''
                    SELECT
                        MIN(humidity) AS min_humidity,
                        MAX(humidity) AS max_humidity,
                        DATE(forecast_date) AS day
                    FROM
                        weather_data
                    GROUP BY
                        day
                    ORDER BY
                        day
                    ''')
    dataset = cursor.fetchall()
    cursor.close()
    organized_data = []
    for data in dataset:
        organized_data.append({'day' : str(data[2]), 'min_humidity' : data[0], 'max_humidity' : data[1]})
    return organized_data

#mode = 0 means that we are accessing rain probability, mode = 1 means that we are accessing snow probability
def pick_up_probabilities(db, mode):
    if mode == 0:
        cursor = db.cursor()
        cursor.execute("""
                        SELECT
                            DATE(wd.forecast_date) AS date,
                            pb.rain_prob AS rain_probability
                        FROM
                            weather_data AS wd INNER JOIN probabilities AS pb
                            ON pb.prob_id = wd.id
                        ORDER BY
                            wd.forecast_date
                        """)
        results = cursor.fetchall()
        dataset = list()
        for record in results:
            dataset.append({'day' : str(record[0]), 'probability of rain' : record[1]})
    if mode == 1:
        cursor = db.cursor()
        cursor.execute("""
                        SELECT
                            DATE(wd.forecast_date) AS date,
                            pb.snow_prob AS snow_probability
                        FROM
                            weather_data AS wd INNER JOIN probabilities AS pb
                            ON pb.prob_id = wd.id
                        ORDER BY
                            wd.forecast_date
                        """)
        results = cursor.fetchall()
        dataset = list()
        for record in results:
            dataset.append({'day' : str(record[0]), 'probability of snow' : record[1]})
    return dataset

#Mode = 0 returns list of dictionaries with data for day and hour with temperature higher than the limit of confort zone
#Mode = 1 returns list of dictionaries with data for day and hour with temperature lower than the limit of confort zone
def danger_time_temp(db, mode):
    dataset = list()
    cursor = db.cursor()
    if mode == 0:
        cursor.execute("""
                        SELECT
                            DATE(forecast_date) AS day,
                            TIME(forecast_date) AS time,
                            temperature
                        FROM
                            weather_data
                        WHERE
                            temperature > 32
                        ORDER BY
                            forecast_date
                        """)
    if mode == 1:
        cursor.execute("""
                        SELECT
                            DATE(forecast_date) AS day,
                            TIME(forecast_date) AS time,
                            temperature
                        FROM
                            weather_data
                        WHERE
                            temperature < 12
                        ORDER BY
                            forecast_date
                        """)
    results = cursor.fetchall()
    cursor.close()
    for record in results:
        dataset.append({'day' : str(record[0]), 'time' : record[1], 'temperature' : record[2]})
    return dataset

#Mode = 0 returns list of dictionaries with data for day and hour with humidity higher than the limit of confort zone
#Mode = 1 returns list of dictionaries with data for day and hour with humidity lower than the limit of confort zone
def danger_time_humidity(db, mode):
    dataset = list()
    cursor = db.cursor()
    if mode == 0:
        cursor.execute("""
                        SELECT
                            DATE(forecast_date) AS day,
                            TIME(forecast_date) AS time,
                            humidity
                        FROM
                            weather_data
                        WHERE
                            humidity > 70
                        ORDER BY
                            forecast_date
                        """)
    if mode == 1:
        cursor.execute("""
                        SELECT
                            DATE(forecast_date) AS day,
                            TIME(forecast_date) AS time,
                            humidity
                        FROM
                            weather_data
                        WHERE
                            humidity < 20
                        ORDER BY
                            forecast_date
                        """)
    results = cursor.fetchall()
    cursor.close()
    for record in results:
        dataset.append({'day' : str(record[0]), 'time' : record[1], 'humidity' : record[2]})
    return dataset

def get_precipt_info(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        DATE(forecast_date) AS day,
                        SUM(precipitation) AS precipt_mm_sum,
                        CASE
                            WHEN SUM(precipitation) = 0.0 THEN 'No rain'
                            WHEN 0.0 < SUM(precipitation) AND SUM(precipitation) <= 10.0 THEN 'Moderate rain'
                            WHEN 10.0 < SUM(precipitation) AND SUM(precipitation) <= 50.0 THEN 'heavy rain'
                            WHEN 50.0 < SUM(precipitation) AND SUM(precipitation) <= 200.0 THEN 'extreme rain'
                            WHEN SUM(precipitation) > 200 THEN 'Mega rain'
                        END AS rain_classification
                    FROM
                        weather_data
                    GROUP BY
                        day
                    ORDER BY
                        day
                    """)
    results = cursor.fetchall()
    info = [{'day' : str(record[0]), 'preciptation_mm' : record[1], 'rain class' : record[2]} for record in results]
    cursor.close()
    return info

def get_precipt_for_rainning_hour(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        forecast_date,
                        precipitation
                    FROM
                        weather_data
                    WHERE
                        precipitation > 0.0
                    """)
    results = cursor.fetchall()
    data = [{'date' : str(record[0]), 'precipitation_mm' : record[1]} for record in results]
    return data

def get_current_weather_data(db):
    cursor = db.cursor()
    cursor.execute("""
                    SELECT
                        temperature,
                        wind_speed,
                        humidity,
                        CASE
                            WHEN is_day = 1 THEN 'YES'
                            ELSE 'NO'
                        END as is_day,
                        last_update,
                        cloud
                    FROM
                        current_weather_data
                    """)
    results = cursor.fetchall()
    info = {'current_temp' : results[0][0],
            'current_ws' : results[0][1],
            'humidity' : results[0][2],
            'is day?' : results[0][3],
            'last update' : results[0][4],
            'cloud' : results[0][5]}
    return info

if __name__ == '__main__':
    import CRUD_DDL as crud_ddl
    my_db = crud_ddl.define_conn()
    print(min_max_temp(my_db))