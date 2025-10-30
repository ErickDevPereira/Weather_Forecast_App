import mysql.connector as conn

def input_as_string(username, password):
    names = {'username' : username, 'password' : password}
    for name, obj in names.items():
        if not isinstance(obj, str):
            raise TypeError(f"Automate_creation() function accepts string at {name}, nothing else.\nYou've used {type(obj)}")

"""
The following function is responsible for the automation of the creation of the tables
and creation of the database. It must be implemented at the beginning of the main.py module.
"""
def automate_creation(username, password):

    input_as_string(username, password)
    
    db = conn.connect(
                host = 'localhost',
                user = username,
                password = password
                    )
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE if not exists forecast')
    cursor.close()
    db.close()
    db = conn.connect(
                    host = 'localhost',
                    user = username,
                    password = password,
                    database = 'forecast'
                    )
    cursor = db.cursor()
    cursor.execute("""
                    CREATE TABLE if not exists city_data (
                    city_id INT PRIMARY KEY AUTO_INCREMENT,
                    city_name VARCHAR(50) NOT NULL,
                    country VARCHAR(50) NOT NULL
                    )
                    """)
    cursor.close()
    cursor = db.cursor()
    cursor.execute("""
                    CREATE TABLE if not exists weather_data (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    city_id INT,
                    temperature DECIMAL(5, 2) NOT NULL,
                    will_it_rain TINYINT NOT NULL,
                    will_it_snow TINYINT NOT NULL,
                    forecast_date DATETIME NOT NULL,
                    humidity TINYINT UNSIGNED NOT NULL,
                    precipitation DECIMAL(5, 1) NOT NULL,
                    FOREIGN KEY (city_id) REFERENCES city_data(city_id)
                    )
                    """)
    cursor.close()
    cursor = db.cursor()
    cursor.execute("""
                    CREATE TABLE if not exists probabilities (
                    prob_id INT PRIMARY KEY,
                    rain_prob INT NOT NULL,
                    snow_prob INT NOT NULL,
                    FOREIGN KEY (prob_id) REFERENCES weather_data (id)
                    )
                    """)
    cursor.close()
    cursor = db.cursor()
    cursor.execute(
                    """
                    CREATE TABLE if not exists current_weather_data(
                    temperature DECIMAL(5, 2) NOT NULL,
                    wind_speed DECIMAL(6, 2) NOT NULL,
                    humidity TINYINT UNSIGNED NOT NULL,
                    is_day TINYINT UNSIGNED NOT NULL,
                    last_update DATETIME NOT NULL,
                    cloud TINYINT NOT NULL
                    )
                    """)
    cursor.close()
    cursor_ind_rain = db.cursor()
    cursor_ind_snow = db.cursor()
    """Creating two indexes, one for the column will_it_rain and other for will_it_snow.
    This is quite important because filters over just will_it_rain or over will_it_snow
    are common in this app. So the indexes will turn these queries into faster ones."""
    cursor_ind_rain.execute("CREATE INDEX idx_rain ON weather_data( will_it_rain )")
    cursor_ind_snow.execute("CREATE INDEX idx_snow ON weather_data( will_it_snow )")
    cursor_ind_rain.close()
    cursor_ind_snow.close()

    return db #Returning the connection object

def sanitize_DB(username, password):
    input_as_string(username, password)
    db_finish = conn.connect(
                        host = 'localhost',
                        user = username,
                        password = password
                        )
    cursor = db_finish.cursor()
    cursor.execute('DROP DATABASE if exists forecast')
    cursor.close()
    db_finish.close()

def define_conn(username, password):
    input_as_string(username, password)
    db = conn.connect(
                    host = 'localhost',
                    user = username,
                    password = password,
                    database = 'forecast'
                    )
    return db

def close_conn(db):
    db.close()