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
options = [
    "Calender"
    ]


#this creates a new/updates the user_data file
def save_data():
    user_data_file = open('./data/user_data', 'wb')
    pickle.dump(UserData,user_data_file)
    user_data_file.close()

#this loads existing data
def load_data():
    global UserData
    user_data_file = open('./data/user_data', 'rb')
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
    new_task_selection = tk.StringVar()
    new_task_selection.set("New Task")
    new_task = tk.OptionMenu(main_frame, new_task_selection, *options)
    new_task.pack()
    def onclick_newtask(*args):
        if new_task_selection.get() == "Calender":
            main_frame.destroy()
            calender_window()
        else:
            print("Do nothing")
    new_task_selection.trace("w", onclick_newtask)
    about = tk.Button(main_frame, text="About Me")
    about.pack()
    def onclick_about(e):
        main_frame.destroy()
        about_me_window()
    about.bind("<Button-1>", onclick_about)
    main_frame.pack()

#window for seeing calender stuff
def calender_window():
    calender_frame = tk.Frame(root)
    tk.Label(calender_frame, text="You can schedule new events here and assign them to a date, I'll remind you of any upcoming events. You can also check for all scheduled events.", wraplength=wrap_length).pack()
    add_new_event = tk.Button(calender_frame, text="Add New Event")
    add_new_event.pack()
    def onclick_new_event(e):
        calender_frame.destroy()
        calender_add_new_event_window()
    add_new_event.bind("<Button-1>", onclick_new_event)
    view_events = tk.Button(calender_frame, text="View All Events")
    view_events.pack()
    def onclick_view_events(e):
        calender_frame.destroy()
        calender_view_events_window()
    view_events.bind("<Button-1>", onclick_view_events)
    back = tk.Button(calender_frame, text="Back")
    back.pack()
    def onclick_back(e):
        calender_frame.destroy()
        main_window()
    back.bind("<Button-1>", onclick_back)
    calender_frame.pack()

#window for adding a new event to the calender
def calender_add_new_event_window():
    calender_add_new_event_frame = tk.Frame(root)
    tk.Label(calender_add_new_event_frame, text="Adding new event").pack()
    back = tk.Button(calender_add_new_event_frame, text="Back")
    back.pack()
    def onclick_back(e):
        calender_add_new_event_frame.destroy()
        calender_window()
    back.bind("<Button-1>", onclick_back)
    calender_add_new_event_frame.pack()

def calender_view_events_window():
    calender_view_events_frame = tk.Frame(root)
    tk.Label(calender_view_events_frame, text="Viewing all events").pack()
    back = tk.Button(calender_view_events_frame, text="Back")
    back.pack()
    def onclick_back(e):
        calender_view_events_frame.destroy()
        calender_window()
    back.bind("<Button-1>", onclick_back)
    calender_view_events_frame.pack()

#about screen to display misc info
def about_me_window():
    about_frame = tk.Frame(root)
    tk.Label(about_frame, text="Hi, I'm Pyreah, a simple digital assistant made by TheNyanChicken. I can handle simple tasks such as reminding you of important events and scheduling. With the addition of any other optional modules that can be gotten at <insert hyperlink here>, I can do other things as well. I hope to be of good service.", wraplength=wrap_length).pack()
    back = tk.Button(about_frame, text="Back")
    back.pack()
    def onclick_back(e):
        about_frame.destroy()
        main_window()
    back.bind("<Button-1>", onclick_back)
    about_frame.pack()

# this checks if there is a user_data save file already exists, and if it does not it creates one
def start_up():
    if os.path.isfile('./data/user_data') == False:
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
