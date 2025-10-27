/*DDL AREA*/
CREATE DATABASE if not exists forecast;
DROP DATABASE if exists forecast;
USE forecast; --Turns the forecast DB into the active one

CREATE TABLE if not exists current_weather_data(
    temperature DECIMAL(5, 2) NOT NULL,
    wind_speed DECIMAL(6, 2) NOT NULL,
    humidity TINYINT UNSIGNED NOT NULL,
    is_day TINYINT UNSIGNED NOT NULL,
    last_update DATETIME NOT NULL,
    cloud TINYINT NOT NULL
);
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
); --Table that will store data for the weather where each record will have data for a hour at a day
CREATE TABLE if not exists city_data (
    city_id INT PRIMARY KEY AUTO_INCREMENT,
    city_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
); --Table with data of the city(ies)
CREATE TABLE if not exists probabilities (
    prob_id INT PRIMARY KEY,
    rain_prob INT NOT NULL,
    snow_prob INT NOT NULL,
    FOREIGN KEY (prob_id) REFERENCES weather_data ( id )
); --Table with probabilities of raining or snowing for each day
DROP TABLE city_data;
DROP TABLE weather_data;
/*DML AREA*/
DELETE FROM weather_data;
DELETE FROM city_data;
/*Queries*/
SELECT * FROM city_data;
SELECT * FROM weather_data;
SELECT * FROM probabilities;
SELECT CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS date,
       FORMAT(AVG(temperature), 2) AS avg_temp,
       FORMAT(AVG(wind_speed), 2) AS avg_wind_speed,
       FORMAT(AVG(humidity), 2) AS avg_humidity
FROM weather_data
GROUP BY CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date));

SELECT
    DATE(forecast_date) AS 'Rain day',
    TIME(forecast_date) AS 'Rain hour',
    temperature AS 'temperature (°C)',
    humidity AS 'humidity (%)'
FROM
    weather_data
WHERE
    will_it_rain = 1
ORDER BY forecast_date;

SELECT
    DATE(forecast_date) AS 'Snow day',
    TIME(forecast_date) AS 'Snow hour',
    temperature AS 'temperature (°C)',
    humidity AS 'humidity (%)'
FROM
    weather_data
WHERE
    will_it_snow = 1
ORDER BY forecast_date;

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
    wd.forecast_date;

SELECT
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS raining_day,
    HOUR(forecast_date) AS raining_hour
FROM
    weather_data
WHERE
    will_it_rain = 1
ORDER BY raining_day, raining_hour; --Shows the day and hour that will have rain.

SELECT
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS snowing_day,
    HOUR(forecast_date) AS snowing_hour
FROM
    weather_data
WHERE
    will_it_snow = 1
ORDER BY snowing_day, snowing_hour; --Shows the day and hour that will have snow.

SELECT
    MIN(temperature) AS min_temp, MAX(temperature) AS max_temp,
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS day
FROM
    weather_data
GROUP BY
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date))
ORDER BY
    day;

SELECT
    MIN(humidity) AS min_humidity,
    MAX(humidity) AS max_humidity,
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS day
FROM
    weather_data
GROUP BY
    day
ORDER BY
    day;

SELECT
    CONCAT(YEAR(wd.forecast_date), '-', MONTH(wd.forecast_date), '-', DAY(wd.forecast_date)) AS date,
    pb.rain_prob AS rain_probability
FROM
    weather_data AS wd INNER JOIN probabilities AS pb
    ON pb.prob_id = wd.id
ORDER BY
    wd.forecast_date;

SELECT
    CONCAT(YEAR(wd.forecast_date), '-', MONTH(wd.forecast_date), '-', DAY(wd.forecast_date)) AS date,
    pb.snow_prob AS snow_probability
FROM
    weather_data AS wd INNER JOIN probabilities AS pb
    ON pb.prob_id = wd.id
ORDER BY
    wd.forecast_date;

SELECT
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS day,
    TIME(forecast_date) AS time,
    temperature
FROM
    weather_data
WHERE
    temperature > 32
ORDER BY
    forecast_date;

SELECT
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS day,
    TIME(forecast_date) AS time,
    temperature
FROM
    weather_data
WHERE
    temperature < 12
ORDER BY
    forecast_date;

SELECT
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS day,
    TIME(forecast_date) AS time,
    humidity
FROM
    weather_data
WHERE
    humidity > 70
ORDER BY
    forecast_date;

SELECT
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS day,
    TIME(forecast_date) AS time,
    humidity
FROM
    weather_data
WHERE
    humidity < 20
ORDER BY
    forecast_date;

SELECT
    CONCAT(YEAR(forecast_date), '-', MONTH(forecast_date), '-', DAY(forecast_date)) AS day,
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
    day;

SELECT
    forecast_date,
    precipitation
FROM
    weather_data
WHERE
    precipitation > 0.0;

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
    current_weather_data;