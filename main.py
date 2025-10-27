import customtkinter as ctk
import API_connection
import DB.CRUD_DDL as crud_ddl
import DB.CRUD_DQL as crud_dql
import DB.EntryDB_UI as db_ui
from args import api_args, fe_args
import UI
import graphs
import os
import time

if not os.path.exists('DB/MySQL_fulldata.txt'):
    start = db_ui.StartMySQL()

URL = api_args['url']
token = api_args['token']

f = open('DB/MySQL_fulldata.txt', 'r')
file_lines = f.readlines()
username = file_lines[1]
username = username[0:-1] #Taking out the \n at the end.
password = file_lines[3]
f.close()

try:
    crud_ddl.sanitize_DB(username, password)
    db = crud_ddl.automate_creation(username, password)
except:
    error_screen  = ctk.CTk() #ERROR screen when the connection to the database MySQL is corrupted

    ctk.set_appearance_mode('dark')

    error_screen.geometry('400x200')
    error_screen.resizable(False, False)
    error_screen.title("MySQL ERROR")

    label = ctk.CTkLabel(error_screen,
                        text = 'ERROR: Error while trying to connect to the database.\nCheck if MySQL is installed correctly',
                        text_color = 'red',
                        font = (fe_args['font_family'], 12))
    label.place(relx = 0.5, rely = 0.5, anchor = 'center')
    error_screen.mainloop()
else:
    input_screen = ctk.CTk() #Screen of input

    ctk.set_appearance_mode('dark')

    input_screen.geometry('600x300')
    input_screen.resizable(False, False)
    input_screen.title("Input screen")

    initial_msg = ctk.CTkLabel(input_screen,
                            text = 'Please, type the name of the city that you\nwhat to query forecast data',
                            font = (fe_args['font_family'], 20))
    initial_msg.place(relx = 0.5, rely = 0.2, anchor = 'center')

    input_box = ctk.CTkEntry(input_screen,
                            placeholder_text = 'Name of the city',
                            placeholder_text_color = fe_args['text_color'],
                            text_color = fe_args['text_color'],
                            width = 200,
                            height = 50,
                            corner_radius = 20,
                            fg_color = fe_args['hover_color'],
                            border_color = 'white',
                            font = (fe_args['font_family'], 14))
    input_box.place(relx = 0.5, rely = 0.5, anchor = 'center')

    def query_API():
        if input_box.get() == '':
            error_msg.configure(text = 'please, type something on the input box')
        else:
            conn_status = API_connection.check_if_connection_is_set(input_box.get(), url = URL, token = token)
            if conn_status == 1:
                city_name = input_box.get()
                api_to_db_status, status_code, tot_time_api = API_connection.API_to_DB(db, city_name, url = URL, token = token)
                if api_to_db_status == 1:
                    '''If we get at this scope, it means that the data went to the database successfully'''
                    input_screen.withdraw()
                    weather_data = crud_dql.all_data(db)
                    avg_values_per_date = crud_dql.evaluate_avg_over_group(db)
                    precipitation_raining_hours = crud_dql.get_precipt_for_rainning_hour(db)
                    #Generating the graphical images
                    it = time.time()#Instant time that the graph generation will start
                    graphs.generate_temp_graph(weather_dataset = weather_data, avg_values_per_date = avg_values_per_date, how_to_visualize=1)
                    graphs.generate_humidity_graph(weather_dataset = weather_data, avg_values_per_date = avg_values_per_date, how_to_visualize=1)
                    graphs.generate_temp_graph(weather_dataset = weather_data, avg_values_per_date = avg_values_per_date, how_to_visualize=2)
                    graphs.generate_temp_graph(weather_dataset = weather_data, avg_values_per_date = avg_values_per_date, how_to_visualize=3)
                    graphs.generate_humidity_graph(weather_dataset = weather_data, avg_values_per_date = avg_values_per_date, how_to_visualize=2)
                    graphs.generate_humidity_graph(weather_dataset = weather_data, avg_values_per_date = avg_values_per_date, how_to_visualize=3)
                    graphs.generate_hist_temp(weather_dataset=weather_data)
                    graphs.generate_hist_humidity(weather_dataset=weather_data)
                    graphs.generate_hist_precipitation(weather_dataset=weather_data, precipitation_rainning_hours = precipitation_raining_hours, mode = 0)
                    graphs.generate_hist_precipitation(weather_dataset=weather_data, precipitation_rainning_hours = precipitation_raining_hours, mode = 1)
                    ft = time.time()#Instant time that the graph generation will stop
                    tot_time_graph = f'{ft - it:.2f} sec'
                    my_app = UI.Main_Dashboard(username, password, tot_time_api, tot_time_graph)
                    my_app.start_app()
                else:
                    error_msg.configure(text = f"Problem with connection to the server\nStatus code: {status_code}")
            else:
                error_msg.configure(text = "ERROR: The app can't achieve data for such city")

    send_button = ctk.CTkButton(input_screen,
                                width= 50,
                                height = 50,
                                corner_radius=20,
                                fg_color = fe_args['pattern_color'],
                                hover_color = fe_args['hover_color'],
                                border_width = 2,
                                border_color = 'white',
                                text = 'SUBMIT',
                                text_color = fe_args['text_color'],
                                font = (fe_args['font_family'], 20),
                                command = query_API
                                )
    send_button.place(relx = 0.5, rely = 0.7, anchor = 'center')

    error_msg = ctk.CTkLabel(input_screen,
                            text = '',
                            text_color = 'red',
                            font = (fe_args['font_family'], 10))
    error_msg.place(relx = 0.5, rely = 0.8, anchor = 'center')
    input_screen.mainloop()