import customtkinter as ctk
import DB.CRUD_DDL as ddl

class StartMySQL():

    def __init__(self, width = 500, hight = 400):
        ctk.set_appearance_mode('dark')
        self.root = ctk.CTk()
        self.root.resizable(False, False)
        self.root.geometry(f'{width}x{hight}')
        self.root.title('MySQL / Forecast App connection')
        self.msg = """The app needs your MySQL username and password.\n
The will need the input just for now.
If you wish to input new data here later
click at the 'close connection' button
presented on the options frame.
"""
        self.msg_label = ctk.CTkLabel(self.root,
                                text = self.msg,
                                font = ('cascadia code semibold', 15),
                                text_color = 'white')
        self.msg_label.place(relx = 0.5, rely = 0.2, anchor = 'center')
        self.label_un = ctk.CTkLabel(self.root,
                                    text = 'Username',
                                    font = ('cascadia code semibold', 18),
                                    text_color = 'white')
        self.label_un.place(relx = 0.2, rely = 0.35)
        self.entry_un = ctk.CTkEntry(self.root,
                                    fg_color = 'black',
                                    placeholder_text = "type 'root' if you don't know your username",
                                    width = 300,
                                    height = 50,
                                    font = ('cascadia code semibold', 10))
        self.entry_un.place(relx = 0.2, rely = 0.42)
        self.label_pw = ctk.CTkLabel(self.root,
                                    text = 'Password',
                                    font = ('cascadia code semibold', 18),
                                    text_color = 'white')
        self.label_pw.place(relx = 0.2, rely = 0.55)
        self.entry_pw = ctk.CTkEntry(self.root,
                                    fg_color = 'black',
                                    placeholder_text = "type the password created during instalation of MySQL",
                                    width = 300,
                                    height = 50,
                                    font = ('cascadia code semibold', 10))
        self.entry_pw.place(relx = 0.2, rely = 0.62)
        self.send_button = ctk.CTkButton(self.root,
                                        fg_color = '#20B2AA',
                                        hover_color = '#008080',
                                        text = 'SELECT',
                                        text_color = 'black',
                                        width = 100,
                                        height = 40,
                                        font = ('cascadia code semibold', 18),
                                        border_width = 2,
                                        border_color = 'black',
                                        command = self.get_mysql)
        self.send_button.place(relx = 0.5, rely = 0.83, anchor = 'center')
        self.cant_op_label = ctk.CTkLabel(self.root,
                                          text = '',
                                          text_color = 'red',
                                          font = ('cascadia code semibold', 12))
        self.cant_op_label.place(relx = 0.5, rely = 0.95, anchor = 'center')
        self.root.mainloop()
    
    def get_mysql(self):
        un = self.entry_un.get()
        pw = self.entry_pw.get()
        if bool(self.entry_un.get()) == False or bool(self.entry_pw.get()) == False:
            self.cant_op_label.configure(text = 'Please, fill all boxes')
        else:
            try:
                db = ddl.define_conn(un, pw)
            except:
                self.cant_op_label.configure(text = 'Username or password incorrect! Did you install MySQL?')
            else:
                f = open('DB/MySQL_fulldata.txt', 'a')
                f.write(f"Username:\n{un}\n")
                f.write(f"Password:\n{pw}")
                f.close()
                db.close()
                self.root.destroy()

if __name__ == '__main__':
    my_app = StartMySQL()