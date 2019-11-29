from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from datetime import date
from datetime import datetime
from math import ceil
import matplotlib.pyplot as plt
import numpy as np

def retrieve_data():
    with open('data.txt','r') as f:
        data = f.read().split(r"%%//%%")[:-1]
    data = [eval(task) for task in data]
    return data

with open('date.txt','r') as f:
    cont = eval(f.read().strip().split("\n")[1])
    d = f.read().strip().split("\n")[0]

def date_conversion(date):
    date = date.split("-")
    month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

    mon=date[1]
    if int(date[2]) in [1,21,31]:
        date[2] = str(date[2]) + "st"
    elif int(date[2]) in [2,22]:
        date[2] = str(date[2]) + "nd"
    elif int(date[2]) in [3,23]:
        date[2] = str(date[2]) + "rd"
    elif int(date[2]) in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
        date[2] = str(date[2]) + "th"
    return "{} {}, {}".format(date[2],month[int(mon)],str(date[0]))

def get_todays_events(pk):
    date = datetime.today().strftime(r'%Y-%m-%d')
    data = retrieve_data()
    cont = data[pk]["data"]
    tasks = []
    for dic in cont:
        pub_date = dic["date"]
        if pub_date==date:
            tasks.append(dic)
    return tasks

def graph_display(pk):
    wnd = Tk()
    
    wnd.geometry("400x200+150+150")
    wnd.config(bg="#A9DFBF")
    wnd.title("Select Range Of Dates")
    wnd.iconbitmap('logo.ico')

    Label(wnd,text="Select A Date",font=('Calistoga',20,"bold"),bg="#A9DFBF",fg="#515A5A").pack()
    Label(wnd,text="",bg="#A9DFBF").pack()

    startDateEntry = ttk.Entry(wnd,font=('Calistoga',20,"bold"))
    startDateEntry.pack()
    Label(wnd,text="",bg="#A9DFBF").pack()

    def graphing(pk):
        s_date = startDateEntry.get()
        wnd.destroy()
        if len(s_date.split("-")[0])!=4 or len(s_date.split("-")[1])!=2 or len(s_date.split("-")[2])!=2:
                messagebox.showerror('Invalid Date.','Enter a Valid Date')
                graph_display(pk)
                
        dates = []
        for i in range(0, 6):
            base = s_date.split("-")[:2]
            add = int(s_date.split("-")[2])-i
            if len(str(add))==1:
                add = "0"+str(add)
            base.append(str(add))
            st=""
            for s in base:
                st+=s
                if base.index(s)!=2:
                    st+="-"
            dates.append(st)

        x = np.arange(6)
        data = retrieve_data()
        tasks = data[pk]["data"]
        matched_dates = []
        for task in tasks:
            if task["date"] in dates:
                matched_dates.append(task["date"])
        req_counts = [0,0,0,0,0,0]
        for i in matched_dates:
            req_counts[dates.index(i)] += 1
            
        #req_counts--> Today, Yesterday,...

        plt.plot(x,req_counts,'bo',ls="solid",markersize=5,markeredgecolor="red")
        plt.xticks(x,dates)
        plt.xlabel("Last Six Days")
        plt.ylabel("No. of Tasks")
        plt.title("Productivity Statistics")
        plt.show()
        
    Button(wnd,text="SUBMIT",bg="#D98880",fg="white",font=('Calistoga',20,"bold"),command=lambda var=pk: graphing(var)).pack()

    wnd.mainloop()


def old_homepage(pk,date=d,tasks=cont[:2]):
    wnd = Toplevel()
    wnd.attributes("-fullscreen", True)
    wnd.configure(bg="#FFE5B4")
    wnd.bind("<Escape>", lambda event: wnd.attributes("-fullscreen", False))
    wnd.title("Day-Task Planner")
    wnd.iconbitmap('logo.ico')

    title_frame = Frame(wnd,bg="#FFE5B4")
    for i in range(3):
        Label(title_frame,text="\t\t\t\t\t\t\t", bg="#FFE5B4").grid(row=0,column=i,pady=5)
    title_font = ('Calistoga',40,"bold")
    current_date_viewed = Label(title_frame,text="Viewing: "+date_conversion(date),font=('Calistoga',20,"bold"),bg="#FFE5B4",fg="black")
    current_date_viewed.grid(row=1,column=0)

    title = Label(title_frame,text=" Day-to-Day Planner",font=('Calistoga',40,"bold underline"),bg="#FFE5B4",fg="black")
    title.grid(row=1,column=1)

    def destroy():
        wnd.destroy()
    back = PhotoImage(master=wnd,file="exit.png")
    back_button = Button(wnd, command=destroy)
    back_button.config(image=back)
    back_button.grid(row=1,column=2)

    Label(title_frame,text="\n",bg="#FFE5B4").grid(row=2,columnspan=3)
    
    title_frame.grid(row=0,columnspan=3,padx=50)
    Label(wnd,text=" ",bg="#FFE5B4").grid(row=1,columnspan=3)
    
    #Profile Panel
    profile_pane = Frame(wnd,bg="#FFE5B4",borderwidth=4,relief="groove")
    profile_font = ('Calistoga',20,"bold")
    data = retrieve_data()
    name = Label(profile_pane,text=data[pk]["name"],font=profile_font,bg="#FFE5B4",fg="black")
    name.grid(row=0,column=0)
    time = Label(profile_pane,text=str(datetime.time(datetime.now())).split(".")[0],font=profile_font,bg="#FFE5B4",fg="black")
    time.grid(row=1,column=0)
    date_ = Label(profile_pane,text=date_conversion(datetime.today().strftime(r'%Y-%m-%d')),font=profile_font,bg="#FFE5B4",fg="black")
    date_.grid(row=2,column=0)
    day = Label(profile_pane,text=datetime.today().strftime("%A"),font=profile_font,bg="#FFE5B4",fg="black")
    day.grid(row=3,column=0)
    profile_pane.grid(row=2,column=0,pady=15)    

    Label(wnd,bg="#FFE5B4",text=" ").grid(row=3,column=0)
    Label(wnd,bg="#FFE5B4",text="\n\n").grid(row=4,column=0)

    profile_pane_down = Frame(wnd,bg="#FFE5B4",borderwidth=4,relief="groove")

    if date==datetime.today().strftime(r'%Y-%m-%d'):
        text = "You Have {} \n Tasks/Events Planned\n Today.".format(len(tasks))
    elif date>datetime.today().strftime(r'%Y-%m-%d'):
        text = "You Have {} \n Tasks/Events Planned\nOn {}.".format(len(tasks),date_conversion(date))
    else:
        text = "You Had {} \n Tasks/Events Planned\n On {}.".format(len(tasks),date_conversion(date))
    reminder = Label(profile_pane_down,text=text,font=profile_font,bg="#FFE5B4",fg="black")
    reminder.grid(row=1,column=0)
    profile_pane_down.grid(row=5,column=0)

    #TASKS PANEL
    def tasks_display(tasks):
        task_panel = Frame(wnd,bg="#FFE5B4",borderwidth=2,relief="solid")
        Label(task_panel,text="\tYour Tasks\t",bg="#FFE5B4",fg="black",font=("Heletivca",25,"bold")).grid(row=0,column=0)
        
        task_font = ("Heletivca",15,"bold")
        task_info_font = ("Heletivca",18,"bold")
        task_number_font = ("Times",20,"bold")
        cur=1
        for task in tasks:
            taskwise_panel = Frame(task_panel,bg="#FFE5B4",borderwidth=4,relief="solid")
            Label(taskwise_panel,text="Task {}".format(data[pk]["data"].index(task)+1),bg="#FFE5B4",font=task_number_font,fg="black").grid(row=0,column=0)
            task_name = Label(taskwise_panel,text=task["task_name"],bg="#FFE5B4",fg="black",font=("Heletivca",25,"bold underline"))
            task_name.grid(row=1,column=0)
            
            length = len(task["task"])
            original = task["task"]
            final = ""
            if length>25:
                while length>25:
                    if length>50:
                        final += task["task"][:25]+"\n"
                        task["task"] = task["task"][25:]
                        length-=25
                    else:
                        final += task["task"][:25]
                        task["task"] = task["task"][25:]
                        length-=25
            else:
                final=task["task"]
            task["task"] = original
                
            task_info = Label(taskwise_panel,text=final,bg="#FFE5B4",fg="black",font=task_info_font)
            task_info.grid(row=2,column=0)
            task_date = Label(taskwise_panel,text=date_conversion(task["date"]),bg="#FFE5B4",fg="black",font=task_font)
            task_date.grid(row=3,column=0)
            task_time = Label(taskwise_panel,text=task["time"],bg="#FFE5B4",fg="black",font=task_font)
            task_time.grid(row=4,column=0)
            taskwise_panel.grid(row=cur,column=0,pady=10)
            cur+=1

        task_panel.grid(row=1,column=1,rowspan=10)
    tasks_display(tasks)

    buttons_frame = Frame(wnd,bg="#FFE5B4")

    Label(buttons_frame,text="\n\n",bg="#FFE5B4").grid(row=1,column=0)
    change_date_img = PhotoImage(master=wnd,file='calendar.png')
    change_date = Button(buttons_frame,command=lambda var=pk: date_selection(var))
    change_date.config(image=change_date_img)
    change_date.grid(row=2,column=0)

    buttons_frame.grid(row=1,column=2,rowspan=10)
    wnd.mainloop()

def add_task(pk):
    wnd = Tk()
    wnd.geometry("400x800+150+20")
    wnd.config(bg="black")
    wnd.title("Add Task!")
    wnd.iconbitmap('logo.ico')

    Label(wnd,text="Add A New Task Here",font=('Calistoga',20,"bold"),bg="black",fg="white").pack()
    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()

    name = Label(wnd,text="Task Name",font=('Calistoga',20,"bold"),bg="black",fg="white")
    name.pack()
    nameEntry = ttk.Entry(wnd,width=100,font=('Calistoga',15))
    nameEntry.insert(0,'Homework')
    nameEntry.pack()

    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()
    info = Label(wnd,text="Task Information",font=('Calistoga',20,"bold"),bg="black",fg="white")
    info.pack()
    infoEntry = scrolledtext.ScrolledText(
        master = wnd,
        wrap   = WORD,
        width  = 25,
        height = 5)

    infoEntry.pack(padx=10, pady=10, fill=BOTH)
    infoEntry.insert(INSERT,"Enter Task Information here...")
    infoEntry.config(font=('Calistoga',15))

    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()

    date = Label(wnd,text="Date of Task",font=('Calistoga',20,"bold"),bg="black",fg="white")
    date.pack()
    dateEntry = ttk.Entry(wnd,width=100,font=('Calistoga',15))
    dateEntry.insert(0,'2019-1-1')
    dateEntry.pack()

    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()

    time = Label(wnd,text="Time of Task",font=('Calistoga',20,"bold"),bg="black",fg="white")
    time.pack()
    timeEntry = ttk.Entry(wnd,width=100,font=('Calistoga',15))
    timeEntry.insert(0,'23:59')
    timeEntry.pack()
    
    Label(wnd,text="",font=('Calistoga',20,"bold underline"),bg="black",fg="white").pack()
    def adding_task():
        name = nameEntry.get()
        info = infoEntry.get(1.0,END)
        date = dateEntry.get()
        time = timeEntry.get()

        def check(date, time):
            if len(date.split("-")[0])!=4 or len(date.split("-")[1])!=2 or len(date.split("-")[2])!=2:
                messagebox.showerror('Invalid Date.','Enter a Valid Date')
                add_task(pk)
            if len(time.split(":")[0])!=2 or len(time.split(":")[1])!=2:
                messagebox.showerror('Invalid Time.','Enter a Valid Time of Day')
                add_task(pk)

        if len(name)==0 or len(info)==0 or len(date)==0 or len(time)==0:
            messagebox.showerror("Invalid Entries.","Kindly Re-Enter or Ensured that All Fields are Filled.")
            add_task(pk)

        check(date,time)
        
        if date<datetime.today().strftime(r'%Y-%m-%d'):
            messagebox.showerror('Invalid Date.','Enter a Valid Date')
            add_task(pk)
        elif date==datetime.today().strftime(r'%Y-%m-%d') and time<str(datetime.time(datetime.now())).split(".")[0]:
            messagebox.showerror('Invalid Time.','Enter a Valid Time of Day')
            add_task(pk)
        else:
            data = retrieve_data()
            data[pk]["data"].append(
                {
                    "task_name":name,
                    "task":info,
                    "date":date,
                    "time":time,
                    "status":"No"
                }
            )

            with open("data.txt","r+") as f:
                cont = f.read()
                base = eval(cont.split(r"%%//%%")[0])
                base["data"] = data[pk]["data"]
                l = cont.split(r"%%//%%")
                l[0] = str(base)
                l[1] = str(eval(l[1]))

            with open('data.txt','w') as f:
                pass

            for user in l[:-1]:
                with open("data.txt","a") as f:
                    f.write(user.strip())
                    f.write("\n%%//%%\n")

            wnd.destroy()
            messagebox.showinfo("Success!","Task '{}' has been successfully added!".format(name))

    submit = Button(wnd,text="ADD TASK",bg="#B54A35",font=('Calistoga',15,"bold"),fg="white",command=adding_task,relief="groove")
    submit.pack()
    wnd.mainloop()

def date_selection(pk):
    wnd = Tk()
    wnd.geometry("400x200+150+150")
    wnd.config(bg="#A9DFBF")
    wnd.title("Select A Date")
    wnd.iconbitmap('logo.ico')

    Label(wnd,text="Select A Date",font=('Calistoga',20,"bold"),bg="#A9DFBF",fg="#515A5A").pack()
    Label(wnd,text="",bg="#A9DFBF").pack()

    dateselectionEntry = ttk.Entry(wnd,font=('Calistoga',20,"bold"))
    dateselectionEntry.pack()

    Label(wnd,text="",bg="#A9DFBF").pack()

    def select_date():
        date = dateselectionEntry.get()
        wnd.destroy()

        if len(date.split("-")[0])!=4 or len(date.split("-")[1])!=2 or len(date.split("-")[2])!=2:
                messagebox.showerror('Invalid Date.','Enter a Valid Date')
                date_selection(pk)

        data = retrieve_data()

        cont = data[pk]["data"]
        tasks = []
        for dic in cont:
            pub_date = dic["date"]
            if pub_date==date:
                tasks.append(dic)

        with open('date.txt','w') as f:
            f.write(date + "\n")
            f.write(str(tasks))
        
        old_homepage(pk,date=date,tasks=tasks)

    submit = Button(wnd,text="SUBMIT",bg="#D98880",fg="white",font=('Calistoga',20,"bold"),command=select_date)
    submit.pack()
    wnd.mainloop()

    
def homepage(pk):
    wnd = Tk()
    wnd.attributes("-fullscreen", True)
    wnd.configure(bg="#FFE5B4")
    wnd.bind("<Escape>", lambda event: wnd.attributes("-fullscreen", False))
    wnd.title("Day-Task Planner")
    wnd.iconbitmap('logo.ico')

    title_frame = Frame(wnd,bg="#FFE5B4")
    for i in range(3):
        Label(title_frame,text="\t\t\t\t\t\t\t", bg="#FFE5B4").grid(row=0,column=i,pady=5)
    title_font = ('Calistoga',40,"bold")
    with open('date.txt','r') as f:
        date = f.read().strip().split("\n")[0]
    
    def today_view():
        old_homepage(pk,date=datetime.today().strftime(r'%Y-%m-%d'),tasks=get_todays_events(pk))

    today = Button(wnd,text="Today",font=('Calistoga',20,"bold"),bg="#FF2A00",fg="white",command=today_view,width=15)
    today.grid(row=1,column=0)

    title = Label(title_frame,text=" Day-to-Day Planner",font=('Calistoga',40,"bold underline"),bg="#FFE5B4",fg="black")
    title.grid(row=1,column=1)

    close_img = PhotoImage(master=wnd,file="close.png")
    close = Button(wnd,command=lambda cur=wnd: login(cur))
    close.config(image=close_img)
    close.grid(row=1,column=2)

    Label(title_frame,text="\n",bg="#FFE5B4").grid(row=2,columnspan=3)
    
    title_frame.grid(row=0,columnspan=3,padx=50)
    Label(wnd,text=" ",bg="#FFE5B4").grid(row=1,columnspan=3)
    
    #Profile Panel
    profile_pane = Frame(wnd,bg="#FFE5B4",borderwidth=4,relief="groove")
    profile_font = ('Calistoga',20,"bold")
    data = retrieve_data()
    name = Label(profile_pane,text=data[pk]["name"],font=profile_font,bg="#FFE5B4",fg="black")
    name.grid(row=0,column=0)
    time = Label(profile_pane,text=str(datetime.time(datetime.now())).split(".")[0],font=profile_font,bg="#FFE5B4",fg="black")
    time.grid(row=1,column=0)
    date = Label(profile_pane,text=date_conversion(datetime.today().strftime(r'%Y-%m-%d')),font=profile_font,bg="#FFE5B4",fg="black")
    date.grid(row=2,column=0)
    day = Label(profile_pane,text=datetime.today().strftime("%A"),font=profile_font,bg="#FFE5B4",fg="black")
    day.grid(row=3,column=0)
    profile_pane.grid(row=2,column=0,pady=15)    

    Label(wnd,bg="#FFE5B4",text=" ").grid(row=3,column=0)
    Label(wnd,bg="#FFE5B4",text="\n\n").grid(row=4,column=0)

    profile_pane_down = Frame(wnd,bg="#FFE5B4",borderwidth=4,relief="groove")
    text = "You Have/Had {} \n Tasks/Events Planned.".format(len(data[pk]["data"]))
    reminder = Label(profile_pane_down,text=text,font=profile_font,bg="#FFE5B4",fg="black")
    reminder.grid(row=1,column=0)
    profile_pane_down.grid(row=5,column=0)

    #TASKS PANEL
    def tasks_display(tasks):
        task_panel = Frame(wnd,bg="#FFE5B4",borderwidth=2,relief="solid")
        Label(task_panel,text="\tYour Tasks\t",bg="#FFE5B4",fg="black",font=("Heletivca",25,"bold")).grid(row=0,column=0)
        
        task_font = ("Heletivca",15,"bold")
        task_info_font = ("Heletivca",16,"bold")
        task_number_font = ("Times",20,"bold")
        cur=1
        for task in tasks:
            taskwise_panel = Frame(task_panel,bg="#FFE5B4",borderwidth=4,relief="solid")
            Label(taskwise_panel,text="Task {}".format(data[pk]["data"].index(task)+1),bg="#FFE5B4",font=task_number_font,fg="black").grid(row=0,column=0)
            task_name = Label(taskwise_panel,text=task["task_name"],bg="#FFE5B4",fg="black",font=("Heletivca",25,"bold underline"))
            task_name.grid(row=1,column=0)
            
            length = len(task["task"])
            original = task["task"]
            final = ""
            if length>50:
                task["task"] = (task["task"][:51]+"...")
            if length>25:
                while length>25:
                    if length>50:
                        final += task["task"][:25]+"\n"
                        task["task"] = task["task"][25:]
                        length-=25
                    else:
                        final += task["task"][:25]
                        task["task"] = task["task"][25:]
                        length-=25
            else:
                final=task["task"]
            final = final.rstrip()
            task["task"] = original
                
            task_info = Label(taskwise_panel,text=final,bg="#FFE5B4",fg="black",font=task_info_font)
            task_info.grid(row=2,column=0)
            task_date = Label(taskwise_panel,text=date_conversion(task["date"]),bg="#FFE5B4",fg="black",font=task_font)
            task_date.grid(row=3,column=0)
            task_time = Label(taskwise_panel,text=task["time"],bg="#FFE5B4",fg="black",font=task_font)
            task_time.grid(row=4,column=0)
            
            def confirm_task(pk,val):
                data = retrieve_data()
                for t in data[pk]["data"]:
                    if int(t["id"])==int(val):
                        cur = data[pk]["data"][data[pk]["data"].index(t)]
                        break
                
                rem = data[pk]["data"][:data[pk]["data"].index(t)]
                if cur["status"]=="Yes":
                    messagebox.showinfo("Task Incomplete.","Page will be updated upon app restart.")
                    cur["status"]="No"
                else:
                    messagebox.showinfo("Task Complete!","Page will be updated upon app restart.")
                    cur["status"]="Yes"

                rem.append(cur)
                rem.extend(data[pk]["data"][data[pk]["data"].index(t)+1:])
                data[pk]["data"]=rem
                
                with open("data.txt","w") as f:
                    for user in data:
                        f.write(str(user)+"\n")
                        f.write(r"%%//%%"+"\n")
                                    
            done = Checkbutton(taskwise_panel,text="Completed?",variable=task["id"],command=lambda pk=pk, val=task["id"]: confirm_task(pk,val),bg="#FFE5B4")
            if task["status"]=="Yes":
                done.select()
            else:
                done.deselect()

            done.grid(row=5,column=0)
            taskwise_panel.grid(row=cur,column=0,pady=10)
            cur+=1

        def page_based_task(page_number):
            change = data[pk]["data"][2*page_number-2:2*page_number]
            task_panel.grid_forget()
            wnd.update()
            tasks_display(change)

        #page nav
        for i in range(1,ceil(len(data[pk]["data"])/2)+1):
            but = Button(task_panel,text=i,bg="red",fg="white",font=('Helevitica',10,"bold"),command= lambda e=i: page_based_task(e))
            but.grid(row=cur,column=i)

        task_panel.grid(row=1,column=1,rowspan=10)
    tasks_display(data[pk]["data"][:2])

    buttons_frame = Frame(wnd,bg="#FFE5B4")
    
    add_tsk_img = PhotoImage(master=wnd,file="planner.png")
    add_tsk = Button(buttons_frame,command=lambda pk=pk: add_task(pk))
    add_tsk.config(image=add_tsk_img)
    add_tsk.grid(row=0,column=0)
    Label(buttons_frame,text="\n\n",bg="#FFE5B4").grid(row=1,column=0)
    change_date_img = PhotoImage(master=wnd,file='calendar.png')
    change_date = Button(buttons_frame,command=lambda var=pk: date_selection(var))
    change_date.config(image=change_date_img)
    change_date.grid(row=2,column=0)
    '''graph_ = Image.open("productivity.png")
    graph = ImageTk.PhotoImage(graph_)'''
    graph= PhotoImage(master=wnd,file="productivity.png")
    graph_button=Button(wnd,command=lambda var=pk: graph_display(var),relief="groove")
    graph_button.config(image=graph)
    graph_button.grid(row=3,column=0)

    buttons_frame.grid(row=1,column=2,rowspan=10)
    wnd.mainloop()

def login(cur):
    try:
        cur.destroy()
    except:
        pass

    wnd = Tk()
    wnd.geometry("300x350+150+150")
    wnd.config(bg="#FFE5B4")
    wnd.title("Day-Task Planner")
    wnd.iconbitmap('logo.ico')

    Label(wnd,text="LOGIN",font=("Heletivca",28,"bold"),bg="#FFE5B4",fg="black").pack()
    Label(wnd,text="----------------------------------------------------------",font=("Heletivca",4,"bold"),bg="#FFE5B4",fg="black").pack()
    Label(wnd,text="",bg="#FFE5B4").pack()
    Label(wnd,text="USERNAME",font=("Heletivca",24,"bold"),bg="#FFE5B4",fg="black").pack()
    username = ttk.Entry(wnd,font=("Heletivca",16,"bold"))
    username.pack()
    Label(wnd,text="",bg="#FFE5B4").pack()
    Label(wnd,text="PASSWORD",font=("Heletivca",24,"bold"),bg="#FFE5B4",fg="black").pack()
    password = ttk.Entry(wnd,font=("Heletivca",16,"bold"),show="*")
    password.pack()
    Label(wnd,text="",bg="#FFE5B4").pack()

    def authenticate(event):
        usern = username.get()
        pswd = password.get()
        data = retrieve_data()

        c=0
        if len(usern)==0 or len(pswd)==0:
            messagebox.showerror("LoginError","Kindly fill in the Credentials.")
            login(wnd)
        for user in data:
            if user["username"]==usern and user["pass"]==pswd:
                messagebox.showinfo("Authenticated!","Successfully logged in!")
                wnd.destroy()
                c+=1
                homepage(data.index(user))
        if c==0:
            messagebox.showerror("LoginError","Username Entered Does Not Exist.")
            login(wnd)
                    
    submit = Button(wnd,text="SUBMIT",font=("Heletivca",20,"bold"),bg="#386B09",fg="yellow")
    submit.bind('<Button-1>',authenticate)
    submit.pack()
    wnd.mainloop()
    
#login("No Window Yet.")
homepage(0)
