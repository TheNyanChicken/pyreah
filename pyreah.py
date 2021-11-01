import os
import pickle
import tkinter as tk
import datetime

#variables
time = datetime.datetime.now().time()
UserData = {}
UserEvents = []

#variables for the main window
root = tk.Tk()
root.title("Pyreah")
root.resizable(False, False)
root.geometry("300x300")
wrap_length = 300
options = [
    "Calender"
    ]

#this creates a new/updates save files
def save_data():
    user_data_file = open('./data/user_data', 'wb')
    pickle.dump(UserData,user_data_file)
    user_data_file.close()
    
    user_events_file = open('./data/user_events', 'wb')
    pickle.dump(UserEvents,user_events_file)
    user_events_file.close()

#this loads existing data
def load_data():
    global UserData
    global UserEvents
    user_data_file = open('./data/user_data', 'rb')
    UserData = pickle.load(user_data_file)
    user_data_file.close()
    
    user_events_file = open('./data/user_events', 'rb')
    UserEvents = pickle.load(user_events_file)
    user_events_file.close()

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
    root.title("Pyreah - Adding New Event")
    tk.Label(calender_add_new_event_frame, text="Title of Event").pack()
    event_title_input = tk.Entry(calender_add_new_event_frame)
    event_title_input.pack()
    tk.Label(calender_add_new_event_frame, text="Date of Event (Day, Month)").pack()
    event_day_input = tk.Entry(calender_add_new_event_frame, textvariable=tk.IntVar(), width="2")
    event_day_input.pack(side=tk.LEFT, padx="10")
    event_month_input = tk.Entry(calender_add_new_event_frame, textvariable=tk.IntVar(), width="2")
    event_month_input.pack(side=tk.LEFT, padx="10")
    event_confirm = tk.Button(calender_add_new_event_frame, text="Confirm")
    event_confirm.pack()
    def onclick_confirm(e):
        event_day = int(event_day_input.get())
        event_month = int(event_month_input.get())
        if event_day >= 1 and event_day <= 31 and event_month >= 1 and event_month <= 12:
            event_info = {'event_title':event_title_input.get(), 'event_day':event_day, 'event_month':event_month}
            UserEvents.append(event_info)
            calender_add_new_event_frame.destroy()
            calender_window()
    event_confirm.bind("<Button-1>", onclick_confirm)
    back = tk.Button(calender_add_new_event_frame, text="Back")
    back.pack()
    def onclick_back(e):
        calender_add_new_event_frame.destroy()
        calender_window()
    back.bind("<Button-1>", onclick_back)
    calender_add_new_event_frame.pack()

#window for seeing all current events
def calender_view_events_window():
    calender_view_events_frame = tk.Frame(root)
    event_number = 1
    tk.Label(calender_view_events_frame, text="These are all the events you currently have planned:", wraplength=wrap_length).pack()
    scrollbar = tk.Scrollbar(calender_view_events_frame, orient='vertical')
    scrollbar.pack(side="right", fill="y")
    view_events_list = tk.Listbox(calender_view_events_frame, yscrollcommand = scrollbar.set)
    for events in UserEvents:
        event_text = str(event_number) + ". " + events['event_title'] + " at " + str(events['event_day']) + "/" + str(events['event_month'])
        view_events_list.insert('end', event_text)
        event_number = event_number + 1
    scrollbar.config(command=view_events_list.yview,)
    view_events_list.pack(side='left', fill='both')
    delete = tk.Button(calender_view_events_frame, text="Delete Event")
    delete.pack(side="top")
    def onclick_delete(e):
        selection = view_events_list.curselection()
        del UserEvents[selection[0]]
        view_events_list.delete(selection[0])
        save_data()
    delete.bind("<Button-1>", onclick_delete)
    back = tk.Button(calender_view_events_frame, text="Back")
    back.pack(side="bottom")
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
save_data()
