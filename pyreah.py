import os
import pickle
import tkinter as tk
import datetime

#variables
time = datetime.datetime.now().time()
UserData = {
    "name":""
    }

#variables for the main window
root = tk.Tk()
root.title("Pyreah")
root.geometry("300x300")
wrap_length = 300

#this creates a new/updates the user_data file
def save_data():
    user_data_file = open('user_data', 'wb')
    pickle.dump(UserData,user_data_file)
    user_data_file.close()

#this loads existing data
def load_data():
    global UserData
    user_data_file = open('user_data', 'rb')
    UserData = pickle.load(user_data_file)
    user_data_file.close()

#main menu
def main_window():
    load_data()
    root.title("Pyreah")
    main_frame = tk.Frame(root)
    if time.hour < 12:
        tk.Label(main_frame, text="Good morning,").pack()
    elif time.hour < 18:
        tk.Label(main_frame, text="Good afternoon,").pack()
    else:
        tk.Label(main_frame, text="Good evening,").pack()
    tk.Label(main_frame, text=UserData["name"]).pack()
    tk.Label(main_frame).pack()
    new_task = tk.Button(main_frame, text="New Task")
    new_task.pack()
    about = tk.Button(main_frame, text="About Me")
    about.pack()
    def onclick_new_task(e):
        main_frame.destroy()
        new_task_window()
    new_task.bind("<Button-1>", onclick_new_task)
    def onclick_about(e):
        main_frame.destroy()
        about_me_window()
    about.bind("<Button-1>", onclick_about)
    main_frame.pack()

def new_task_window():
    new_task_frame = tk.Frame(root)
    tk.Label(new_task_frame, text="I can do these things for you:").pack()
    back = tk.Button(new_task_frame, text="Back")
    back.pack()
    def onclick_back(e):
        new_task_frame.destroy()
        main_window()
    back.bind("<Button-1>", onclick_back)
    new_task_frame.pack()

def about_me_window():
    about_frame = tk.Frame(root)
    tk.Label(about_frame, text="Hi, I'm Pyreah, a simple digital assistant made by Froginator. I can handle simple tasks such as reminding you of important events and scheduling. With the addition of any other optional modules that can be gotten at <insert hyperlink here>, I can do other things as well. I hope to be of good service.", wraplength=wrap_length).pack()
    back = tk.Button(about_frame, text="Back")
    back.pack()
    def onclick_back(e):
        about_frame.destroy()
        main_window()
    back.bind("<Button-1>", onclick_back)
    about_frame.pack()

# this checks if there is a user_data save file already exists, and if it does not it creates one
def start_up():
    if os.path.isfile('./user_data') == False:
        root.title("Pyreah - Setup")
        setup_frame = tk.Frame(root)
        setup_frame.pack()
        tk.Label(setup_frame,text="Hello, since this is the first time meeting each other, we should introduce ourselves. I am Pyreah, a very simple digital assistant. What should I call you?",wraplength=wrap_length).pack()
        set_name = tk.Entry(setup_frame)
        set_name.pack()
        def keypress(e):
            UserData["name"] = set_name.get()
            setup_frame.pack()
            setup_frame.destroy()
            save_data()
            main_window()
        root.bind("<Return>", keypress)
    else:
        main_window()

start_up()
root.mainloop()
