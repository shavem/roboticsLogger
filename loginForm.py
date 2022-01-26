import os
from tkinter import *
from tkinter.ttk import Style
from tkinter import messagebox
import pandas as pd
from datetime import datetime
from github import Github

# Github stuff
user = "RoboticsLogger"
with open("password.txt", "r") as f:
    password = f.readline()
g = Github(password)


def gitDownload():
    repo = g.get_user().get_repo('RoboticsLog')  # repo name

    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    # Download from github
    git_prefix = ''
    git_file = git_prefix + 'RoboticsHourLog.csv'
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        with open("RoboticsHourLog.csv", "wb") as f:
            f.write(contents.decoded_content)
    else:
        print("Repo does not contain the csv file")


def gitUpload():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    day = now.weekday()
    day_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    commit_message = "Updated " + date + " (" + day_of_the_week[day] + ")"

    repo = g.get_user().get_repo('RoboticsLog')  # repo name

    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    with open('RoboticsHourLog.csv', 'r') as file:
        content = file.read()

    # Upload to github
    git_prefix = ''
    git_file = git_prefix + 'RoboticsHourLog.csv'
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, commit_message, content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, commit_message, content, branch="main")
        print(git_file + ' CREATED')

    return commit_message


# File import
gitDownload()
df = pd.read_csv("RoboticsHourLog.csv")
df.to_csv("RoboticsHourLog.csv", index=False)

# Create cache to store all people that have signed in and not signed out
signed_in = []

# Reset today's date and create column if needed
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
if not current_date in df.columns:
    df[current_date] = ""


# Time manipulation functions
def time_difference(start_time, end_time):
    og = start_time.split(":")
    new = end_time.split(":")
    return (int((new[0])) - int(og[0])) * 3600 + (int(new[1]) - int(og[1])) * 60 + (int(new[2]) - int(og[2]))


def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)


def time_to_seconds(time):
    hours = int(time.split(":")[0])
    minutes = int(time.split(":")[1])
    seconds = int(time.split(":")[2])
    return hours * 3600 + minutes * 60 + seconds


# Converts a list into a string
def list_to_string(list):
    string = ""
    for i in list:
        string += i + ", "
    return string[:-2]


# root window

# TODO: Add the robotics icon
root = Tk()
root.title("Robotics Sign-In Form")


# Closing
def on_closing(df):
    # TODO: open new window allowing user to input number of hours for people that haven't signed out
    if len(signed_in) > 0:
        if messagebox.askokcancel("Quit",
                                  f"Do you want to quit? The following people have not signed out and will be set to a default of 1 hour: {list_to_string(signed_in)}"):
            # TODO: set default hours for people who didn't sign out and add the "not signed out" attribute
            for name in signed_in:
                seconds_to_add = 1 * 60 * 60

                df.loc[df.index[df["Name"] == name].tolist()[0], current_date] += f" - Not Signed Out: default 1 hour"
                df.loc[df.index[df["Name"] == name].tolist()[0], "Hours"] = seconds_to_time(
                    time_to_seconds(df.loc[df.index[df["Name"] == name].tolist()[0], "Hours"]) + seconds_to_add)
                print(f"{name} not signed out (default 1 hour)")
            save_df = df.sort_values(by=["Hours"], ascending=False, key=lambda x: x.str.split(":").str.get(0).astype(int))
            save_df.to_csv("RoboticsHourLog.csv", index=False)
            message = gitUpload()
            save_df.to_csv(f"backup/{message}.csv", index=False)
            print(save_df)
            try:
                os.remove("RoboticsHourLog.csv")
                print("Removed successfully")
            except OSError as error:
                print(error)
                print("File path can not be removed")
            root.destroy()
    else:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            save_df = df.sort_values(by=["Hours"], ascending=False, key=lambda x: x.str.split(":").str.get(0).astype(int))
            save_df.to_csv("RoboticsHourLog.csv", index=False)
            message = gitUpload()
            save_df.to_csv(f"backup/{message}.csv", index=False)
            print(save_df)
            try:
                os.remove("RoboticsHourLog.csv")
                print("Removed successfully")
            except OSError as error:
                print(error)
                print("File path can not be removed")
            root.destroy()


root.protocol("WM_DELETE_WINDOW", lambda: on_closing(df))

# Instructions
myLabel = Label(root, text="Find for your name:")

# Pick name
name_frame = Frame(root)
# Scrollbar
name_scrollbar = Scrollbar(name_frame, orient=VERTICAL)
name_box = Listbox(name_frame, yscrollcommand=name_scrollbar.set, width=30)
name_scrollbar.config(command=name_box.yview)

names = []
# Populate listbox
for row in df.iterrows():
    name_box.insert(END, row[1]["Name"])
    names.append(row[1]["Name"])
# Set initial selection
name_box.select_set(0)


# Buttons
def save():
    name = name_box.get(name_box.curselection())
    if messagebox.askyesno("Save", f"Do you want to {r.get()} {name}?"):
        # TODO: Be able to sign in multiple people at once
        if r.get() == "sign in":
            if name in signed_in:
                messagebox.showerror("Error", f"{name} has already signed in")
            else:
                signed_in.append(name)
                now = datetime.now()
                df.loc[df.index[df["Name"] == name].tolist()[0], current_date] = now.strftime("%H:%M:%S")
                print(f"{name} signed in at {now.strftime('%H:%M:%S')}")
        elif r.get() == "sign out":
            if name not in signed_in:
                messagebox.showerror("Error", f"{name} has not signed in")
            else:
                signed_in.remove(name)
                now = datetime.now()
                hours_to_add = time_difference(df.loc[df.index[df["Name"] == name].tolist()[0], current_date],
                                               now.strftime("%H:%M:%S"))
                df.loc[df.index[df["Name"] == name].tolist()[0], current_date] += f" - {now.strftime('%H:%M:%S')}"
                df.loc[df.index[df["Name"] == name].tolist()[0], "Hours"] = seconds_to_time(
                    time_to_seconds(df.loc[df.index[df["Name"] == name].tolist()[0], "Hours"]) + hours_to_add)
                print(f"{name} signed out at {now.strftime('%H:%M:%S')}")
        else:
            print("Error: invalid input")


radioFrame = LabelFrame(root)

r = StringVar()
r.set("sign in")

search = StringVar()
search.set("")

sign_in_radio = Radiobutton(radioFrame, text="Sign-in", variable=r, value="sign in", background="light green")
sign_out_radio = Radiobutton(radioFrame, text="Sign-out", variable=r, value="sign out", background="tomato")

save_button = Button(root, text="Save", command=save)

# Pack stuff
myLabel.pack()
name_scrollbar.pack(side=RIGHT, fill=Y)
name_box.pack(pady=10, padx=10, side=LEFT, fill=BOTH, expand=True)
name_box.focus_set()
name_frame.pack()
sign_in_radio.grid(row=0, column=0)
style = Style(root)
sign_out_radio.grid(row=0, column=1)
radioFrame.pack()
save_button.pack()

# Key bindings
root.bind("<Return>", lambda event: save())
root.bind("<Left>", lambda event: r.set("sign in"))
root.bind("<Right>", lambda event: r.set("sign out"))
root.bind("<Up>", lambda event: name_box.curselection()[0] - 1 if name_box.curselection()[0] > 0 else 0)
root.bind("<Down>",
          lambda event: name_box.curselection()[0] + 1 if name_box.curselection()[0] < len(names) - 1 else len(
              names) - 1)
root.bind("<Escape>", lambda event: on_closing(df))


def listbox_search(event):
    search.set(search.get() + event.char)
    search_string = search.get()
    found = False
    for i in range(len(names)):
        if names[i].lower().startswith(search_string):
            name_box.select_clear(0, END)
            name_box.select_set(i)
            event.widget.see(i)
            name_box.event_generate("<<ListboxSelect>>")
            name_box.see(i)
            print(search_string)
            found = True
            break
    if not found:
        for i in range(len(names)):
            if search_string in names[i].lower():
                name_box.select_clear(0, END)
                name_box.selection_set(i)
                name_box.see(i)
                print(search_string)
                found = True
                break
    if not found:
        search.set("")
        print("search cleared")


root.bind("<Key>", lambda event: listbox_search(event))

root.mainloop()
