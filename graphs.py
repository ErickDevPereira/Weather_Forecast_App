import matplotlib.pyplot as plt
import numpy as np
import DB.CRUD_DQL as crud_dql
import DB.CRUD_DDL as crud_ddl
import args
import aux_functions

def set_color(color, visibility = True):
    ax = plt.gca()
    ax.tick_params(axis = 'x', colors = color)
    ax.tick_params(axis = 'y', colors = color)
    if visibility:
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
    else:
        for spine in ax.spines.values():
            spine.set_visible(visibility)
        
"""
For the following 3 functions will save an image in the folder graphical_img.
Detail i: weather_dataset will receive data for every day and every hour. weather_dataset must be linked to all_data().
Detail ii: avg_values_per_date will receive average data for each one of the 3 days. avg_values_per_date msut be linked to evaluate_avg_over_group().
Detail iii: how_to_visualize receives 1, 2 or 3. 1 means curve graph, 2 means pie chart and 3 means bar graph.
All these functions have this bahavior
"""

def generate_temp_graph(weather_dataset, avg_values_per_date, how_to_visualize):
    set_color('white')
    #title_font = {'family' : 'monospace', 'color' : 'white', 'size' : 22}
    axis_label_font = {'family' : 'monospace', 'color' : 'white', 'size' : 18}
    avg_temp = np.array([
                        avg_values_per_date[0]['avg_temp'],
                        avg_values_per_date[1]['avg_temp'],
                        avg_values_per_date[2]['avg_temp']
                        ])
    if how_to_visualize == 1:
        #Solving the required mathematical operations
        x_data = np.arange(0, 24 * 3)
        y_continuos_data = np.array([weather_dataset[i]['temperature'] for i in range(24 * 3)])
        y1, y2, y3 = np.zeros((24,)), np.zeros((24,)), np.zeros((24,))
        y1[:] = avg_temp[0]
        y2[:] = avg_temp[1]
        y3[:] = avg_temp[2]
        y_group_data = np.hstack((y1, y2, y3))
        #Defining the image
        plt.grid(axis = 'y', linestyle = '--')
        #plt.title('Temperature graph', fontdict = title_font)
        plt.xlabel('days', fontdict = axis_label_font)
        plt.ylabel('temperature (°C)', fontdict = axis_label_font)
        plt.xticks([12, 24 + 12, 24 * 2 + 12], [avg_values_per_date[0]['date'], avg_values_per_date[1]['date'], avg_values_per_date[2]['date']])
        plt.plot(x_data, y_continuos_data, color = 'orange', label = 'hourly data')
        plt.plot(x_data, y_group_data, color = 'red', label = 'daily average data')
        plt.legend(title = 'Type of data')
        plt.xlim(0, 24*3 - 1)
        #Saving the image
        plt.savefig('graphical_img/temp_img/temp_graph', dpi = 300, transparent = True)
    elif how_to_visualize == 2:
        days = ["--->".join([avg_values_per_date[0]['date'], str(avg_values_per_date[0]['avg_temp']) + "°C"]),
                "--->".join([avg_values_per_date[1]['date'], str(avg_values_per_date[1]['avg_temp']) + "°C"]),
                "--->".join([avg_values_per_date[2]['date'], str(avg_values_per_date[2]['avg_temp']) + "°C"])]
        #plt.title('Average temperature for each day', fontdict = title_font)
        plt.pie(avg_temp, colors = [args.fe_args['avg_color_day1'],
                                                   args.fe_args['avg_color_day2'],
                                                   args.fe_args['avg_color_day3']])
        plt.legend(labels = days)
        plt.savefig('graphical_img/temp_img/temp_pie', dpi = 300, transparent = True)
    elif how_to_visualize == 3:
        days = [avg_values_per_date[0]['date'], avg_values_per_date[1]['date'], avg_values_per_date[2]['date']]
        #plt.title('Average temperature for each day', fontdict = title_font)
        plt.xlabel('days', fontdict = axis_label_font)
        plt.ylabel('average temperature (°C)', fontdict = axis_label_font)
        plt.bar(days, avg_temp, color = [args.fe_args['avg_color_day1'],
                                         args.fe_args['avg_color_day2'],
                                         args.fe_args['avg_color_day3']])
        plt.savefig('graphical_img/temp_img/temp_bar', dpi = 300, transparent = True)
    plt.clf()

def generate_humidity_graph(weather_dataset, avg_values_per_date, how_to_visualize):
    set_color('white')
    title_font = {'family' : 'monospace', 'color' : 'white', 'size' : 16}
    axis_label_font = {'family' : 'monospace', 'color' : 'white', 'size' : 12}
    avg_humidity = np.array([
                        avg_values_per_date[0]['avg_humidity'],
                        avg_values_per_date[1]['avg_humidity'],
                        avg_values_per_date[2]['avg_humidity']
                        ])
    if how_to_visualize == 1:
        #Solving the required mathematical operations
        x_data = np.arange(0, 24 * 3)
        y_continuos_data = np.array([weather_dataset[i]['humidity'] for i in range(24 * 3)])
        y1, y2, y3 = np.zeros((24,)), np.zeros((24,)), np.zeros((24,))
        y1[:] = avg_humidity[0]
        y2[:] = avg_humidity[1]
        y3[:] = avg_humidity[2]
        y_group_data = np.hstack((y1, y2, y3))
        #Defining the image
        plt.grid(axis = 'y', linestyle = '--')
        #plt.title('Humidity graph', fontdict = title_font)
        plt.xlabel('days', fontdict = axis_label_font)
        plt.ylabel('humidity (%)', fontdict = axis_label_font)
        plt.xticks([12, 24 + 12, 24 * 2 + 12], [avg_values_per_date[0]['date'], avg_values_per_date[1]['date'], avg_values_per_date[2]['date']])
        plt.plot(x_data, y_continuos_data, color = 'orange')
        plt.plot(x_data, y_group_data, color = 'red')
        plt.xlim(0, 24*3 - 1)
        plt.ylim(0, 100)
        #Saving the image
        plt.savefig('graphical_img/humidity_img/humidity_graph', dpi = 300, transparent = True)
    elif how_to_visualize == 2:
        days = [avg_values_per_date[0]['date'],
                avg_values_per_date[1]['date'],
                avg_values_per_date[2]['date']]
        #plt.title('Average humidity for each day', fontdict = title_font)
        plt.pie(avg_humidity, autopct = '%.2f%%',colors = [args.fe_args['avg_color_day1'],
                                                       args.fe_args['avg_color_day2'],
                                                       args.fe_args['avg_color_day3']])
        plt.legend(labels = days)
        plt.savefig('graphical_img/humidity_img/humidity_pie', dpi = 300, transparent = True)
    elif how_to_visualize == 3:
        days = [avg_values_per_date[0]['date'], avg_values_per_date[1]['date'], avg_values_per_date[2]['date']]
        plt.xlabel('days', fontdict = axis_label_font)
        plt.ylabel('average humidity (%)', fontdict = axis_label_font)
        #plt.title('Average humidity for each day', fontdict = title_font)
        plt.bar(days, avg_humidity, color = [args.fe_args['avg_color_day1'],
                                             args.fe_args['avg_color_day2'],
                                             args.fe_args['avg_color_day3']])
        plt.savefig('graphical_img/humidity_img/humidity_bar', dpi = 300, transparent = True)
    plt.clf()

""""
Here, each parameter is linked to a crud_dql function:
my_db = crud_ddl.define_conn()
weather_dataset = crud_dql.all_data(my_db)
avg_values_per_date = crud_dql.evaluate_avg_over_group(my_db)
raining_data = crud_dql.rain_snow_data(my_db, 1)
snowing_data = crud_dql.rain_snow_data(my_db, 0)
"""
def generate_snow_rain_prediction_graph(weather_dataset, avg_values_per_date, raining_data, snowing_data):
    fig, axs = plt.subplots(3, 2)
    fig.suptitle('Rain-Snow analysis')
    hours = np.arange(0, 24)
    #rain signal for the next 3 days
    rain_signal1 = np.array([weather_dataset[i]['will it rain'] for i in range(24)])
    rain_signal2 = np.array([weather_dataset[i]['will it rain'] for i in range(24, 24 * 2)])
    rain_signal3 = np.array([weather_dataset[i]['will it rain'] for i in range(24 * 2, 24 * 3)])
    #Rain signal for the next 3 days
    snow_signal1 = np.array([weather_dataset[i]['will it snow'] for i in range(24)])
    snow_signal2 = np.array([weather_dataset[i]['will it snow'] for i in range(24, 24 * 2)])
    snow_signal3 = np.array([weather_dataset[i]['will it snow'] for i in range(24 * 2, 24 * 3)])
    #Constructing the images for the rain signal for the next 3 days
    day1 = avg_values_per_date[0]['date']
    day2 = avg_values_per_date[1]['date']
    day3 = avg_values_per_date[2]['date']
    #Day 1
    Day1raining = raining_data[day1]
    axs[0, 0].plot(hours, rain_signal1)
    axs[0, 0].set_title(f'Rain analysis for day {avg_values_per_date[0]['date']}')
    axs[0, 0].set_xlabel('hours')
    axs[0, 0].set_ylabel('response')
    axs[0, 0].set_xticks(aux_functions.let_just_the_extreme(Day1raining), aux_functions.let_just_the_extreme(Day1raining))
    axs[0, 0].set_yticks([0, 1], ['No', 'Yes'])
    axs[0, 0].set_ylim(-0.5, 1.5)
    #Day 2
    Day2raining = raining_data[day2]
    axs[1, 0].plot(hours, rain_signal2)
    axs[1, 0].set_title(f'Rain analysis for day {avg_values_per_date[1]['date']}')
    axs[1, 0].set_xlabel('hours')
    axs[1, 0].set_ylabel('response')
    axs[1, 0].set_xticks(aux_functions.let_just_the_extreme(Day2raining), aux_functions.let_just_the_extreme(Day2raining))
    axs[1, 0].set_yticks([0, 1], ['No', 'Yes'])
    axs[1, 0].set_ylim(-0.5, 1.5)
    #Day 3
    Day3raining = raining_data[day3]
    axs[2, 0].plot(hours, rain_signal3)
    axs[2, 0].set_title(f'Rain analysis for day {avg_values_per_date[2]['date']}')
    axs[2, 0].set_xlabel('hours')
    axs[2, 0].set_ylabel('response')
    axs[2, 0].set_xticks(aux_functions.let_just_the_extreme(Day3raining), aux_functions.let_just_the_extreme(Day3raining))
    axs[2, 0].set_yticks([0, 1], ['No', 'Yes'])
    axs[2, 0].set_ylim(-0.5, 1.5)
    plt.tight_layout()
    #Constructing the images for the snow signal for the next 3 days
    #Day 1
    Day1snowing = snowing_data[day1]
    axs[0, 1].plot(hours, snow_signal1)
    axs[0, 1].set_title(f'Snow analysis for day {avg_values_per_date[0]['date']}')
    axs[0, 1].set_xlabel('hours')
    axs[0, 1].set_ylabel('response')
    axs[0, 1].set_xticks(aux_functions.let_just_the_extreme(Day1snowing), aux_functions.let_just_the_extreme(Day1snowing))
    axs[0, 1].set_yticks([0, 1], ['No', 'Yes'])
    axs[0, 1].set_ylim(-0.5, 1.5)
    #Day 2
    Day2snowing = snowing_data[day2]
    axs[1, 1].plot(hours, snow_signal2)
    axs[1, 1].set_title(f'Snow analysis for day {avg_values_per_date[1]['date']}')
    axs[1, 1].set_xlabel('hours')
    axs[1, 1].set_ylabel('response')
    axs[1, 1].set_xticks(aux_functions.let_just_the_extreme(Day2snowing), aux_functions.let_just_the_extreme(Day2snowing))
    axs[1, 1].set_yticks([0, 1], ['No', 'Yes'])
    axs[1, 1].set_ylim(-0.5, 1.5)
    #Day 3
    Day3snowing = snowing_data[day3]
    axs[2, 1].plot(hours, snow_signal3)
    axs[2, 1].set_title(f'Snow analysis for day {avg_values_per_date[2]['date']}')
    axs[2, 1].set_xlabel('hours')
    axs[2, 1].set_ylabel('response')
    axs[2, 1].set_xticks(aux_functions.let_just_the_extreme(Day3snowing), aux_functions.let_just_the_extreme(Day3snowing))
    axs[2, 1].set_yticks([0, 1], ['No', 'Yes'])
    axs[2, 1].set_ylim(-0.5, 1.5)
    plt.tight_layout()
    plt.show()
'''
Here, the function is defined considering that the parameters will take:
rain_prob_data = crud_dql.pick_up_probabilities(db, 0)
snow_prob_data = crud_dql.pick_up_probabilities(db, 1)
db is the connection object linked to forecast database.
'''
def generate_snow_rain_prob_graph(rain_prob_data, snow_prob_data):
    days = np.unique(np.array([rain_prob_data[i]['day'] for i in range(24 * 3)]))
    range_hour = np.arange(0, 24)
    day1 = days[0]
    day2 = days[1]
    day3 = days[2]
    rainProbData = np.array([rain_prob_data[i]['probability of rain'] for i in range(24 * 3)])
    snowProbData = np.array([snow_prob_data[i]['probability of snow'] for i in range(24 * 3)])
    splitted_in_days_rain = np.array_split(rainProbData, 3)
    rainData1, rainData2, rainData3 = splitted_in_days_rain[0], splitted_in_days_rain[1], splitted_in_days_rain[2]
    splitted_in_days_snow = np.array_split(snowProbData, 3)
    snowData1, snowData2, snowData3 = splitted_in_days_snow[0], splitted_in_days_snow[1], splitted_in_days_snow[2]
    fig, axs = plt.subplots(3, 2)
    fig.suptitle('Probability graphs for each day')
    #Setting the labels and titles
    for i in range(3):
        for j in range(2):
            if i == 0:
                if j == 0:
                    axs[i, j].set_title(f'Rain {day1}')
                else:
                    axs[i, j].set_title(f'Snow {day1}')
            elif i == 1:
                if j == 0:
                    axs[i, j].set_title(f'Rain {day2}')
                else:
                    axs[i, j].set_title(f'Snow {day2}')
            else:
                if j == 0:
                    axs[i, j].set_title(f'Rain {day3}')
                else:
                    axs[i, j].set_title(f'Snow {day3}')
            axs[i, j].set_ylim(-10, 110)
            axs[i, j].set_xlabel('Hours')
            axs[i, j].set_ylabel('Probability (%)')
            axs[i, j].set_yticks([0, 25, 50, 75, 100], ['0 %', '25 %', '50 %', '75 %', '100 %'])
    #Images for the rain data for 3 days forward
    #Day 1
    axs[0, 0].plot(range_hour, rainData1)
    #Day 2
    axs[1, 0].plot(range_hour, rainData2)
    #Day 3
    axs[2, 0].plot(range_hour, rainData3)
    #Images for the snow data for 3 days forward
    #Day 1
    axs[0, 1].plot(range_hour, snowData1)
    #Day 2
    axs[1, 1].plot(range_hour, snowData2)
    #Day 3
    axs[2, 1].plot(range_hour, snowData3)
    plt.tight_layout()
    plt.show()

#weather_dataset must be crud_dql.all_data(my_db)
def generate_hist_temp(weather_dataset):
    set_color('white')
    temp_dataset = [weather_dataset[i]['temperature'] for i in range(24 * 3)]
    plt.title('Temperature distribution considering each hour of 3 days',
                fontdict = {'family' : 'monospace', 'color' : 'white', 'size' : 13})
    plt.xlabel('temperature (°C)',
                fontdict = {'family' : 'monospace', 'color' : 'white', 'size' : 13})
    plt.ylabel('quantity of hours',
                fontdict = {'family' : 'monospace', 'color' : 'white', 'size' : 13})
    plt.hist(temp_dataset,
            bins = 15,
            color = args.fe_args['hover_color'],
            edgecolor = 'black')
    plt.savefig('graphical_img/temp_img/histogram_temp', dpi = 300, transparent = True)
    plt.clf()

#weather_dataset must be crud_dql.all_data(my_db)
def generate_hist_humidity(weather_dataset):
    set_color('white')
    hum_dataset = [weather_dataset[i]['humidity'] for i in range(24 * 3)]
    #plt.title('Humidity distribution considering each hour of 3 days',
    #            fontdict = {'family' : 'monospace', 'color' : 'white', 'size' : 13})
    plt.xlabel('humidity (%)',
                fontdict = {'family' : 'monospace', 'color' : 'white', 'size' : 13})
    plt.ylabel('quantity of hours',
                fontdict = {'family' : 'monospace', 'color' : 'white', 'size' : 13})
    plt.hist(hum_dataset,
            bins = 15,
            color = args.fe_args['hover_color'],
            edgecolor = 'black')
    plt.savefig('graphical_img/humidity_img/histogram_humidity', dpi = 300, transparent = True)
    plt.clf()

#weather_dataset must be crud_dql.all_data(my_db)
#precipitation_rainning_hours must be crud_dql.get_precipt_for_rainning_hour(my_db)
def generate_hist_precipitation(weather_dataset, precipitation_rainning_hours, mode):
    set_color('white')
    font_title = {'family' : 'monospace', 'color' : 'white', 'size' : 14}
    font_label = {'family' : 'monospace', 'color' : 'white', 'size' : 18}
    if mode == 0:
        prec_dataset = [weather_dataset[i]['precipitation'] for i in range(24 * 3)]
        plt.title('Precipitation distribution for the next 3 days',
                    fontdict = font_title)
        plt.xlabel('precipitation (mm)',
                    fontdict = font_label)
        plt.ylabel('quantity of hours',
                    fontdict = font_label)
        plt.hist(prec_dataset,
                bins = 15,
                color = args.fe_args['hover_color'],
                edgecolor = 'black')
        plt.savefig('graphical_img/rain_and_snow/histogram_precipitation_overall', dpi = 300, transparent = True)
    if mode == 1:
        size = len(precipitation_rainning_hours)
        prec_dataset = [precipitation_rainning_hours[i]['precipitation_mm'] for i in range(size)]
        plt.title('Precipitation considering raining hours',
                    fontdict = font_title)
        plt.xlabel('precipitation (mm)',
                    fontdict = font_label)
        plt.ylabel('quantity of hours',
                    fontdict = font_label)
        plt.hist(prec_dataset,
                bins = 15,
                color = args.fe_args['hover_color'],
                edgecolor = 'black')
        plt.savefig('graphical_img/rain_and_snow/histogram_precipitation_rainfall', dpi = 300, transparent = True)
    plt.clf()

def generate_bar_amount_mm_animation(weather_data, avg_values_per_date, time = 0.5):
    plt.xlabel('days')
    plt.ylabel('Rain amount (mm)')
    days = np.array_split(np.array(weather_data), 3)
    day1_dataset = days[0]
    day2_dataset = days[1]
    day3_dataset = days[2]
    day1 = aux_functions.transform_date(avg_values_per_date[0]['date'])
    day2 = aux_functions.transform_date(avg_values_per_date[1]['date'])
    day3 = aux_functions.transform_date(avg_values_per_date[2]['date'])
    full_amount = np.zeros((3,))
    for hour in range(0, 24):
        full_amount[0] += float(day1_dataset[hour]['precipitation'])
        full_amount[1] += float(day2_dataset[hour]['precipitation'])
        full_amount[2] += float(day3_dataset[hour]['precipitation'])
    max_mm = np.max(full_amount) #Maximum amount for the next 3 days.
    amount_day1 = 0
    amount_day2 = 0
    amount_day3 = 0
    plt.ylim(0, max_mm + 2)
    for hour in range(0, 24):
        plt.title(f'Amount of precipitation\nHour {hour}AM') if hour < 12 else plt.title(f'Amount of precipitation\nHour {hour - 12}PM')
        amount_day1 += day1_dataset[hour]['precipitation']
        amount_day2 += day2_dataset[hour]['precipitation']
        amount_day3 += day3_dataset[hour]['precipitation']
        plt.bar([day1, day2, day3], [amount_day1, amount_day2, amount_day3], color = ['green', 'blue', 'orange'])
        plt.pause(time)

if __name__ == '__main__': #Scope used for tests inside this script
    db = crud_ddl.define_conn('root', 'Ichigo007*')
    weather_data = crud_dql.all_data(db)
    avg_values_per_date = crud_dql.evaluate_avg_over_group(db)
    generate_bar_amount_mm_animation(weather_data, avg_values_per_date)