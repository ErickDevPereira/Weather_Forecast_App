'''If mode is 1, it will change the city_data, but if mode is 0, it will fill weather data'''
def charge_DB(db, /, *,city_id, city_name, country, temperature, will_it_rain, will_it_snow, forecast_date, humidity, precipitation, prob_id, rain_prob, snow_prob,
              cur_temp, cur_ws, cur_hum, cur_is_day, cur_last_update, cur_cloud, mode = None):
    cursor = db.cursor()
    if mode == 1:
        cursor.execute("""INSERT INTO city_data (city_id, city_name, country) VALUES
                    (%s, %s, %s)""", (city_id, city_name, country))
    if mode == 0:
        cursor.execute("""
                        INSERT INTO weather_data (city_id, temperature, will_it_rain, will_it_snow, forecast_date, humidity, precipitation)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (city_id, temperature, will_it_rain, will_it_snow, forecast_date, humidity, precipitation))
    if mode == -1:
        cursor.execute('INSERT INTO probabilities VALUES (%s, %s, %s)', (prob_id, rain_prob, snow_prob))
    if mode is None:
        cursor.execute('INSERT INTO current_weather_data VALUES (%s, %s, %s, %s, %s, %s)',
                       (cur_temp, cur_ws, cur_hum, cur_is_day, cur_last_update, cur_cloud))
    db.commit()
    cursor.close()