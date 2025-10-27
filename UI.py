import customtkinter as ctk
from PIL import Image
import DB.CRUD_DQL as crud_dql
import DB.CRUD_DDL as crud_ddl
import args
import aux_functions
from graphs import generate_snow_rain_prediction_graph, generate_snow_rain_prob_graph, generate_bar_amount_mm_animation
import os

"""Class that will define a pattern for any window from now on.
I implemented it here in order to reuse code later throughout inheritance."""
class Widget:

    class Button:

        def __init__(self, *, text, surface, x, y, call_function,
                    mode = 'center',
                    width = 150,
                    height = 50,
                    color = args.fe_args['pattern_color'],
                    hcolor = args.fe_args['hover_color'],
                    text_color = 'black',
                    font_fam = 'cascadia code semibold',
                    font_size = 17,
                    border_color = 'black',
                    border_width = 2,
                    image_path = None):
            self.x = x
            self.y = y
            self.mode = mode
            self.color = color
            self.hcolor = hcolor
            self.width = width
            self.height = height
            self.text = text
            if image_path is not None:
                self.icon = ctk.CTkImage(light_image=Image.open(image_path))
                self.but = ctk.CTkButton(surface,
                                    text = self.text,
                                    text_color = text_color,
                                    width = self.width,
                                    height = self.height,
                                    fg_color = self.color,
                                    hover_color = self.hcolor,
                                    command = call_function,
                                    font = (font_fam, font_size),
                                    border_color = border_color,
                                    border_width = border_width,
                                    image = self.icon)
            else:
                self.but = ctk.CTkButton(surface,
                                    text = self.text,
                                    text_color = text_color,
                                    width = self.width,
                                    height = self.height,
                                    fg_color = self.color,
                                    hover_color = self.hcolor,
                                    command = call_function,
                                    font = (font_fam, font_size),
                                    border_color = border_color,
                                    border_width = border_width)
            self.but.place(relx = self.x, rely = self.y, anchor = self.mode)

        def deactivate_button(self):
            self.but.configure(state = 'disabled')
        
    class Img:

        def __init__(self, *, surface, path_IMG, width, height, x, y, mode = 'center'):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.IMG = ctk.CTkImage(light_image = Image.open(path_IMG), size = (width, height))
            self.IMG_lab = ctk.CTkLabel(surface, text = '', image = self.IMG)
            self.IMG_lab.place(relx = x, rely = y, anchor = mode)
    
    class TxtBox:

        def __init__(self, *, surface, width, height, font_size, x, y,
                    font_fam = args.fe_args['font_family'],
                    mode = 'nw'):
            self.width = width
            self.height = height
            self.font_size = font_size
            self.x = x
            self.y = y
            self.txt = ctk.CTkTextbox(surface,
                                    width = self.width,
                                    height = self.height,
                                    font = (font_fam, self.font_size))
            self.txt.place(relx = self.x, rely = self.y, anchor = mode)
        
        def write(self, text):
            self.txt.insert('end', text)
        
        def deactivate(self):
            self.txt.configure(state = 'disable')

class Screen:

    def __init__(self, width = 1000, height = 650, title = 'Weather Dashboard Area'):
        self.width = width
        self.height = height
        self.title = title
        ctk.set_appearance_mode('dark')
        self.app = ctk.CTkToplevel()
        self.app.geometry(f'{self.width}x{self.height}')
        self.app.title(title)
        self.app.resizable(False, False)
    
    def start_app(self):
        self.app.mainloop()

class Main_Dashboard(Screen, Widget):

    def __init__(self, username, password, tot_time_api = '0.00 sec', tot_time_graph = '0.00 sec',
                 font_fam = 'cascadia code semibold'):
        super().__init__()
        self.frame_opt = ctk.CTkFrame(self.app, width = 200, height = 650)
        self.title = ctk.CTkLabel(self.frame_opt,
                                  text = 'WELCOME TO\nMY FORECAST APP',
                                  font = (font_fam, 20))
        self.title.place(relx = 0.5, rely = 0.1, anchor = 'center')
        self.thunderIMG = self.Img(surface = self.frame_opt,
                                   path_IMG = 'dashboards_img/thunder.png',
                                   width = 70,
                                   height = 70,
                                   x = 0.5,
                                   y = 0.25) #Thunder Image defined here
        self.frame_opt.place(relx = 0.0, rely = 0.0)
        self.overall_but = self.Button(surface = self.frame_opt,
                    x = 0.5,
                    y = 0.4,
                    call_function = self.call_overall_widgets,
                    text = 'Overall') #Overall button
        self.rain_but = self.Button(surface = self.frame_opt,
                    x = 0.5,
                    y = 0.5,
                    call_function = self.call_rain_widgets,
                    text = 'Precipitation') #Rain button
        self.temp_but = self.Button(surface = self.frame_opt,
                    x = 0.5,
                    y = 0.6,
                    call_function = self.call_temp_widgets,
                    text = 'Temperature') #Temperature button
        self.hum_but = self.Button(surface = self.frame_opt,
                    x = 0.5,
                    y = 0.7,
                    call_function = self.call_humidity_widgets,
                    text = 'Humidity') #Humidity button
        self.label_close_conn = ctk.CTkLabel(self.frame_opt,
                                            text = 'Close connection',
                                            font = (args.fe_args['font_family'], 14))
        self.label_close_conn.place(relx = 0.04, rely = 0.8)
        self.close_conn_button = self.Button(surface = self.frame_opt,
                                            text = 'X',
                                            color = 'red',
                                            hcolor = '#8B0000',
                                            x = 0.8,
                                            y = 0.8,
                                            width = 30,
                                            height = 30,
                                            call_function = self.close_conn,
                                            mode = 'nw')
        self.tot_time_DBAPI = ctk.CTkLabel(self.frame_opt,
                                    text = f'Time for downloading from WeatherAPI\n and charging MySQL database: {tot_time_api}',
                                    font = ('arial', 10))
        self.tot_time_DBAPI.place(relx = 0.01, rely = 0.9)
        self.tot_time_graph = ctk.CTkLabel(self.frame_opt,
                                        text = f'Time to create graphs: {tot_time_graph}',
                                        font = ('arial', 10))
        self.tot_time_graph.place(relx = 0.01, rely = 0.95)
        self.create_frame()
        self.my_db = crud_ddl.define_conn(username, password)
        self.avg_dataset = crud_dql.evaluate_avg_over_group(self.my_db)
        self.call_overall_widgets(first_call = True)

    def rm_frame(self):
        self.main_frame.destroy()
    
    def create_frame(self):
        self.main_frame = ctk.CTkFrame(self.app,
                                        width = 770,
                                        height = 610)
        self.main_frame.place(relx = 0.22, rely = 0.04)
    
    def close_conn(self):
        if os.path.exists('DB/MySQL_fulldata.txt'):
            os.remove('DB/MySQL_fulldata.txt')
        self.app.destroy()

    def call_temp_widgets(self):
        self.rm_frame()
        self.create_frame()
        self.temp_frame_info = ctk.CTkFrame(self.main_frame,
                                            width = 740,
                                            height = 160)
        self.temp_frame_info.place(relx = 0.02, rely = 0.02)
        self.dates = [aux_functions.transform_date(self.avg_dataset[ind]['date']) for ind in range(3)]
        self.avg_temp = [self.avg_dataset[ind]['avg_temp'] for ind in range(3)]
        self.temp_images = {'low' : 'dashboards_img/low_temp.png',
                            'high' : 'dashboards_img/high_temp.png',
                            'regular' : 'dashboards_img/standard.png'}
        #Average Temperature
        self.avg_temp_msg = ctk.CTkLabel(self.temp_frame_info,
                                        text = 'Average Temperatures',
                                        font = (args.fe_args['font_family'], 18))
        self.avg_temp_msg.place(relx = 0.02, rely = 0.04)
        y_pos = (0.25, 0.48, 0.73)
        for ind in range(3):
            self.avg_temp_lab = ctk.CTkLabel(self.temp_frame_info,
                                        text = f"{self.dates[ind]} : {self.avg_temp[ind]}°C",
                                        font = (args.fe_args['font_family'], 18))
            self.avg_temp_lab.place(relx = 0.02, rely = y_pos[ind])
            if self.avg_temp[ind] > 32:
                self.highTempIMG = self.Img(surface = self.temp_frame_info,
                                            path_IMG = self.temp_images['hight'],
                                            x = 0.27,
                                            y = y_pos[ind],
                                            mode = 'nw',
                                            width = 30,
                                            height = 30)
            elif self.avg_temp[ind] < 12:
                self.lowTempIMG = self.Img(surface = self.temp_frame_info,
                                            path_IMG = self.temp_images['low'],
                                            x = 0.27,
                                            y = y_pos[ind],
                                            mode = 'nw',
                                            width = 30,
                                            height = 30)
            else:
                self.regTempIMG = self.Img(surface = self.temp_frame_info,
                                           path_IMG = self.temp_images['regular'],
                                           x = 0.27,
                                           y = y_pos[ind],
                                           width = 30,
                                           height = 30,
                                           mode = 'nw')
        self.DangerTxtTemp = self.TxtBox(surface = self.temp_frame_info,
                                        width = 270,
                                        height = 145,
                                        font_fam= args.fe_args['font_family'],
                                        font_size = 15,
                                        x = 0.33,
                                        y = 0.05)
        self.danger_temp_str_low, self.danger_temp_str_high = aux_functions.get_temp_danger_info(self.my_db)
        self.DangerTxtTemp.write(self.danger_temp_str_low)
        self.DangerTxtTemp.write(self.danger_temp_str_high)
        self.DangerTxtTemp.deactivate()
        self.DangerTxtTemp_ = self.TxtBox(surface = self.temp_frame_info,
                                        width = 200,
                                        height = 145,
                                        font_fam= args.fe_args['font_family'],
                                        font_size = 15,
                                        x = 0.71,
                                        y = 0.05)
        self.extremes_temp_str = aux_functions.get_extreme_temp_per_day(self.my_db)
        self.DangerTxtTemp_.write(self.extremes_temp_str)
        self.DangerTxtTemp_.deactivate()
        self.graphic_info_frame = ctk.CTkFrame(self.main_frame,
                                            width = 740,
                                            height = 415)
        self.graphic_info_frame.place(relx = 0.02, rely = 0.3)
        self.TempHistIMG = self.Img(surface = self.graphic_info_frame,
                                    path_IMG = 'graphical_img/temp_img/histogram_temp.png',
                                    x = 0.01,
                                    y = -0.04,
                                    width = 315,
                                    height = 230,
                                    mode = 'nw')
        self.TempBarIMG = self.Img(surface = self.graphic_info_frame,
                                    path_IMG = 'graphical_img/temp_img/temp_bar.png',
                                    x = 0.55,
                                    y = 0.5,
                                    width = 300,
                                    height = 200,
                                    mode = 'nw')
        self.TempBarIMG = self.Img(surface = self.graphic_info_frame,
                                    path_IMG = 'graphical_img/temp_img/temp_pie.png',
                                    x = 0.53,
                                    y = -0.05,
                                    width = 340,
                                    height = 230,
                                    mode = 'nw')
        self.TempGraphIMG = self.Img(surface = self.graphic_info_frame,
                                    path_IMG = 'graphical_img/temp_img/temp_graph.png',
                                    x = 0.01,
                                    y = 0.5,
                                    width = 340,
                                    height = 200,
                                    mode = 'nw')

    def generate_overall_widget_set(self, img_path, status, width_img = 90, height_img = 90):
        self.overall_frame = ctk.CTkFrame(self.main_frame, width = 450, height = 200)
        self.overall_frame.place(relx = 0.02, rely = 0.02)
        self.IMG_cm = ctk.CTkImage(light_image=Image.open(img_path), size = (width_img, height_img))
        self.img_cm = ctk.CTkLabel(self.overall_frame, text = '', image = self.IMG_cm)
        self.img_cm.place(relx = 0.2, rely = 0.44, anchor = 'center')
        self.city = crud_dql.all_data(self.my_db)[0]['city name']
        self.country = crud_dql.all_data(self.my_db)[0]['country']
        self.loc = ctk.CTkLabel(self.overall_frame,
                                text = f'Location: {self.city}, {self.country}',
                                font = (args.fe_args['font_family'], 17))
        self.loc.place(relx = 0.5, rely = 0.1, anchor = 'center')
        self.msg_current_temp = ctk.CTkLabel(self.overall_frame,
                                            text = f'{self.current_dataset['current_temp']} °C',
                                            font = (args.fe_args['font_family'], 22))
        self.msg_current_temp.place(relx = 0.2, rely = 0.75, anchor = 'center')
        self.msg_current_status = ctk.CTkLabel(self.overall_frame,
                                            text = f'Status: {status}',
                                            font = (args.fe_args['font_family'], 17))
        self.msg_current_status.place(relx = 0.37, rely = 0.24)
        self.msg_current_hum = ctk.CTkLabel(self.overall_frame,
                                            text = f'Humidity: {self.current_dataset['humidity']}%',
                                            font = (args.fe_args['font_family'], 17))
        self.msg_current_hum.place(relx = 0.37, rely = 0.39)
        self.msg_current_ws = ctk.CTkLabel(self.overall_frame,
                                        text = f'Wind Speed: {self.current_dataset['current_ws']} km/h',
                                        font = (args.fe_args['font_family'], 17))
        self.msg_current_ws.place(relx = 0.37, rely = 0.56)
        self.msg_current_lu = ctk.CTkLabel(self.overall_frame,
                                        text = f'Last update: {aux_functions.beaulty_date(str(self.current_dataset['last update']))}',
                                        font = (args.fe_args['font_family'], 17))
        self.msg_current_lu.place(relx = 0.09, rely = 0.8)

    def call_overall_widgets(self, first_call = False):
        self.current_dataset = crud_dql.get_current_weather_data(self.my_db)
        if not first_call:
            self.rm_frame()
            self.create_frame()
        if self.current_dataset['is day?'] == 'NO':
            if self.current_dataset['cloud'] >= 50:
                self.generate_overall_widget_set(img_path = 'dashboards_img/cloudly_moon.png', status = 'Partially cloud')
            else:
                self.generate_overall_widget_set(img_path = 'dashboards_img/Moon.png', status = 'Clean sky')
        else:
            if self.current_dataset['cloud'] >= 50:
                self.generate_overall_widget_set(img_path = 'dashboards_img/cloudly_sun.png', status = 'Partially cloud')
            else:
                self.generate_overall_widget_set(img_path = 'dashboards_img/sun.png', status = 'Clean sky')
        self.temp_avg_frame = ctk.CTkFrame(self.main_frame,
                                           width = 260,
                                           height = 200)
        self.temp_avg_frame.place(relx = 0.64, rely = 0.02)
        self.temp_title = ctk.CTkLabel(self.temp_avg_frame,
                                    text = 'Average temperature\nfor the next 3 days',
                                    font = (args.fe_args['font_family'], 20))
        self.temp_title.place(relx = 0.05, rely = 0.05)
        self.avg_temp_lab1 = ctk.CTkLabel(self.temp_avg_frame,
                                    text = f"{aux_functions.transform_date(self.avg_dataset[0]['date'])} {self.avg_dataset[0]['avg_temp']}°C\n",
                                    font = (args.fe_args['font_family'], 20))
        self.avg_temp_lab1.place(relx = 0.15, rely = 0.4)
        self.avg_temp_lab1 = ctk.CTkLabel(self.temp_avg_frame,
                                    text = f"{aux_functions.transform_date(self.avg_dataset[1]['date'])} {self.avg_dataset[1]['avg_temp']}°C\n",
                                    font = (args.fe_args['font_family'], 20))
        self.avg_temp_lab1.place(relx = 0.15, rely = 0.6)
        self.avg_temp_lab1 = ctk.CTkLabel(self.temp_avg_frame,
                                    text = f"{aux_functions.transform_date(self.avg_dataset[2]['date'])} {self.avg_dataset[2]['avg_temp']}°C",
                                    font = (args.fe_args['font_family'], 20))
        self.avg_temp_lab1.place(relx = 0.15, rely = 0.78)
        self.bottom_frame = ctk.CTkFrame(self.main_frame,
                                                width = 740,
                                                height = 375)
        self.bottom_frame.place(relx = 0.02, rely = 0.37)
        self.dist_prec_graph_link = 'graphical_img/rain_and_snow/histogram_precipitation_overall.png'
        self.disc_prec_graph_IMG = self.Img(surface = self.bottom_frame,
                                            x = -0.02,
                                            y = 0.03,
                                            path_IMG = self.dist_prec_graph_link,
                                            width = 400,
                                            height = 300,
                                            mode = 'nw')
        self.temp_graph_link = 'graphical_img/temp_img/temp_graph.png'
        self.temp_graph_IMG = self.Img(surface = self.bottom_frame,
                                            x = 0.51,
                                            y = 0.06,
                                            path_IMG = self.temp_graph_link,
                                            width = 390,
                                            height = 280,
                                            mode = 'nw')
        
    def call_rain_widgets(self):
        self.rm_frame()
        self.create_frame()
        self.top_frame = ctk.CTkFrame(self.main_frame,
                                    width = 740,
                                    height = 160)
        self.top_frame.place(relx = 0.02, rely = 0.02)
        self.label_mm_tot = ctk.CTkLabel(self.top_frame,
                                        text = 'Total mm precipitation:',
                                        font = (args.fe_args['font_family'], 18))
        self.label_mm_tot.place(relx = 0.02, rely = 0.02)
        self.data = crud_dql.get_precipt_info(self.my_db)
        self.status_images = {'danger' : 'dashboards_img/caution.png',
                            'regular' : 'dashboards_img/standard.png'}
        y_pos = (0.25, 0.48, 0.73)
        for ind in range(3):
            self.amount = ctk.CTkLabel(self.top_frame,
                                    text = f'{aux_functions.transform_date(self.data[ind]['day'])}  {self.data[ind]['preciptation_mm']}mm',
                                    font = (args.fe_args['font_family'], 18))
            self.amount.place(relx = 0.02, rely = y_pos[ind])
            if self.data[ind]['preciptation_mm'] <= 10:
                self.REG_img = self.Img(surface = self.top_frame,
                                            path_IMG = self.status_images['regular'],
                                            x = 0.27,
                                            y = y_pos[ind],
                                            mode = 'nw',
                                            width = 30,
                                            height = 30)
            else:
                self.DANGER_img = self.Img(surface = self.top_frame,
                                            path_IMG = self.status_images['danger'],
                                            x = 0.27,
                                            y = y_pos[ind],
                                            mode = 'nw',
                                            width = 30,
                                            height = 30)
        self.txt_mm_info = self.TxtBox(surface = self.top_frame,
                                       width = 254,
                                       height = 140,
                                       font_size = 12,
                                       x = 0.35,
                                       y = 0.04)
        self.full_info = 'Information for the next 3 days:\n\n'
        for day_data in self.data:
            self.full_info += f'Day >> {aux_functions.transform_date(day_data['day'])}\n'
            self.full_info += f'Amount >> {day_data['preciptation_mm']}mm\n'
            self.full_info += f'Status >> {day_data['rain class']}\n\n'
        self.txt_mm_info.write(text = self.full_info)
        self.prob_but_lab = ctk.CTkLabel(self.top_frame,
                                        text = 'Probabilities',
                                        font = (args.fe_args['font_family'], 18))
        self.prob_but_lab.place(relx = 0.71, rely = 0.08, anchor = 'nw')
        self.prob_but = self.Button(surface = self.top_frame,
                                    width = 40,
                                    height = 40,
                                    x = 0.94,
                                    y = 0.07,
                                    call_function = self.show_prob,
                                    text = '',
                                    mode = 'nw',
                                    image_path = 'dashboards_img/Lupa.png')
        self.will_it_rain_but_lab = ctk.CTkLabel(self.top_frame,
                                        text = 'Rainning days',
                                        font = (args.fe_args['font_family'], 18))
        self.will_it_rain_but_lab.place(relx = 0.71, rely = 0.4, anchor = 'nw')
        self.will_it_rain_but = self.Button(surface = self.top_frame,
                                    width = 40,
                                    height = 40,
                                    x = 0.94,
                                    y = 0.39,
                                    call_function = self.show_will_it_rain,
                                    text = '',
                                    mode = 'nw',
                                    image_path = 'dashboards_img/Lupa.png')
        self.amount_but_lab = ctk.CTkLabel(self.top_frame,
                                        text = 'Amount animation',
                                        font = (args.fe_args['font_family'], 18))
        self.amount_but_lab.place(relx = 0.71, rely = 0.7, anchor = 'nw')
        self.amount_but = self.Button(surface = self.top_frame,
                                    width = 40,
                                    height = 40,
                                    x = 0.94,
                                    y = 0.69,
                                    call_function = self.show_mm_per_day,
                                    text = '',
                                    mode = 'nw',
                                    image_path = 'dashboards_img/Lupa.png')
        self.bottom_fram = ctk.CTkFrame(self.main_frame,
                                        width = 740,
                                        height = 415)
        self.bottom_fram.place(relx = 0.02, rely = 0.3)
        self.only_mm_hist_img = self.Img(surface = self.bottom_fram,
                                    path_IMG = 'graphical_img/rain_and_snow/histogram_precipitation_rainfall.png',
                                    width = 300,
                                    height = 200,
                                    x = 0.01,
                                    y = 0.01,
                                    mode = 'nw')
        self.mm_hist_img = self.Img(surface = self.bottom_fram,
                                    path_IMG = 'graphical_img/rain_and_snow/histogram_precipitation_overall.png',
                                    width = 300,
                                    height = 190,
                                    x = 0.01,
                                    y = 0.5,
                                    mode = 'nw')
        self.full_rain_data = self.TxtBox(surface = self.bottom_fram,
                                        width = 400,
                                        height = 380,
                                        font_size = 15,
                                        x = 0.43,
                                        y = 0.05)
        self.full_rain_data.write(aux_functions.get_rain_data_organized(self.my_db))
        self.full_rain_data.deactivate()
    
    def show_prob(self):
        self.rain_prob_data = crud_dql.pick_up_probabilities(self.my_db, 0)
        self.snow_prob_data = crud_dql.pick_up_probabilities(self.my_db, 1)
        generate_snow_rain_prob_graph(rain_prob_data = self.rain_prob_data, snow_prob_data = self.snow_prob_data)

    def show_will_it_rain(self):
        self.weather_data = crud_dql.all_data(self.my_db)
        self.avg_values_per_date = crud_dql.evaluate_avg_over_group(self.my_db)
        self.raining_data = crud_dql.rain_snow_data(self.my_db, 1)
        self.snowing_data = crud_dql.rain_snow_data(self.my_db, 0)
        generate_snow_rain_prediction_graph(weather_dataset = self.weather_data,
                                            avg_values_per_date = self.avg_values_per_date,
                                            raining_data = self.raining_data,
                                            snowing_data = self.snowing_data)
    
    def show_mm_per_day(self):
        self.weather_data = crud_dql.all_data(self.my_db)
        self.avg_values_per_date = crud_dql.evaluate_avg_over_group(self.my_db)
        generate_bar_amount_mm_animation(self.weather_data, self.avg_values_per_date)

    def call_humidity_widgets(self):
        self.rm_frame()
        self.create_frame()
        self.hum_frame_info = ctk.CTkFrame(self.main_frame,
                                            width = 740,
                                            height = 160)
        self.hum_frame_info.place(relx = 0.02, rely = 0.02)
        self.dates = [aux_functions.transform_date(self.avg_dataset[ind]['date']) for ind in range(3)]
        self.avg_hum = [self.avg_dataset[ind]['avg_humidity'] for ind in range(3)]
        self.hum_images = {'danger' : 'dashboards_img/caution.png',
                            'regular' : 'dashboards_img/standard.png'}
        #Average Humidity
        self.avg_hum_msg = ctk.CTkLabel(self.hum_frame_info,
                                        text = 'Average Humidity',
                                        font = (args.fe_args['font_family'], 18))
        self.avg_hum_msg.place(relx = 0.02, rely = 0.04)
        y_pos = (0.25, 0.48, 0.73)
        for ind in range(3):
            self.avg_hum_lab = ctk.CTkLabel(self.hum_frame_info,
                                        text = f"{self.dates[ind]} : {self.avg_hum[ind]}%",
                                        font = (args.fe_args['font_family'], 18))
            self.avg_hum_lab.place(relx = 0.02, rely = y_pos[ind])
            if self.avg_hum[ind] > 70 or self.avg_hum[ind] < 20:
                self.DANGER_img = self.Img(surface = self.hum_frame_info,
                                            path_IMG = self.hum_images['danger'],
                                            x = 0.27,
                                            y = y_pos[ind],
                                            mode = 'nw',
                                            width = 30,
                                            height = 30)
            else:
                self.REGULAR_img = self.Img(surface = self.hum_frame_info,
                                            path_IMG = self.hum_images['regular'],
                                            x = 0.27,
                                            y = y_pos[ind],
                                            mode = 'nw',
                                            width = 30,
                                            height = 30)
        self.DangerTxtHum = self.TxtBox(surface = self.hum_frame_info,
                                        width = 270,
                                        height = 145,
                                        font_fam= args.fe_args['font_family'],
                                        font_size = 11,
                                        x = 0.33,
                                        y = 0.05)
        self.danger_hum_str_low, self.danger_hum_str_high = aux_functions.get_hum_danger_info(self.my_db)
        self.DangerTxtHum.write(self.danger_hum_str_low)
        self.DangerTxtHum.write(self.danger_hum_str_high)
        self.DangerTxtHum.deactivate()
        self.DangerTxtHum_ = self.TxtBox(surface = self.hum_frame_info,
                                        width = 200,
                                        height = 145,
                                        font_fam= args.fe_args['font_family'],
                                        font_size = 15,
                                        x = 0.71,
                                        y = 0.05)
        self.extremes_hum_str = aux_functions.get_extremes_per_day_hum(self.my_db)
        self.DangerTxtHum_.write(self.extremes_hum_str)
        self.DangerTxtHum_.deactivate()
        self.graphic_info_frame = ctk.CTkFrame(self.main_frame,
                                            width = 740,
                                            height = 415)
        self.graphic_info_frame.place(relx = 0.02, rely = 0.3)
        self.hum_hist_img = self.Img(surface = self.graphic_info_frame,
                                    path_IMG = 'graphical_img/humidity_img/histogram_humidity.png',
                                    width = 315,
                                    height = 230,
                                    x = 0.01,
                                    y = -0.04,
                                    mode = 'nw')
        self.hum_bar_img = self.Img(surface = self.graphic_info_frame,
                                    path_IMG = 'graphical_img/humidity_img/humidity_bar.png',
                                    width = 300,
                                    height = 200,
                                    x = 0.55,
                                    y = 0.5,
                                    mode = 'nw')
        self.hum_pie_img = self.Img(surface = self.graphic_info_frame,
                                    path_IMG = 'graphical_img/humidity_img/humidity_pie.png',
                                    width = 300,
                                    height = 200,
                                    x = 0.53,
                                    y = -0.05,
                                    mode = 'nw')
        self.hum_graph_img = self.Img(surface = self.graphic_info_frame,
                                    path_IMG = 'graphical_img/humidity_img/humidity_graph.png',
                                    width = 340,
                                    height = 200,
                                    x = 0.01,
                                    y = 0.5,
                                    mode = 'nw')

if __name__ == '__main__':
    my_app = Main_Dashboard('root', 'Ichigo007*')
    my_app.start_app()