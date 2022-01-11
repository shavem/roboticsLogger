from tkinter import *
from tkinter.ttk import Style
from tkinter import messagebox
import csv


# TODO: Make it auto-upload to github when closed
# File import
# f = open("RoboticsHourLog.csv", "w")
# csv_reader = csv.reader(f, delimiter=",")
# headers = []
# for row in csv_reader:
#     headers.append(row)
#     break
# print(headers)

# root window

# TODO: Add the robotics icon
root = Tk()
root.title("Robotics Sign-In Form")

# Closing
def on_closing():
    # TODO: decide default hours for someone who doesn't sign out and list them all in this messagebox and ask this messagebox only if there are people that haven't signed out
    if messagebox.askokcancel("Quit", "Do you want to quit? The following people have not signed out and will be set to 'Not Signed Out' with a default of _ hours:"):
        root.destroy()
        # TODO: set default hours for people who didn't sign out and add the "not signed out" attribute
        print("Set everyone to _ hours by default and add 'did not sign out' to it")

root.protocol("WM_DELETE_WINDOW", on_closing)


# Instructions
# TODO: Add a dropdown meny to select the name of the person who is signing in with the ability to type and search for the name
myLabel = Label(root, text="Find for your name:")


# Pick name
# TODO: Make the names ordered by most hours, add keybinds tot he listbox
name_frame = Frame(root)
# Scrollbar
name_scrollbar = Scrollbar(name_frame, orient=VERTICAL)
name_box = Listbox(name_frame, yscrollcommand=name_scrollbar.set)
name_scrollbar.config(command=name_box.yview)
with open("members.txt", "r") as f:
    for line in f:
        name_box.insert(END, line.strip())


# Buttons
def save():
    if messagebox.askyesno("Save", f"Do you want to {r.get()} {name_box.get(name_box.curselection())}?"):
        # TODO: Create signing in and signing out function, be able to sign in multiple people at once
        print(f"{r.get()} {name_box.get(name_box.curselection())}")


radioFrame = LabelFrame(root)

r = StringVar()
r.set("sign in")

sign_in_radio = Radiobutton(radioFrame, text="Sign-in", variable=r, value="sign in", background="light green")
sign_out_radio = Radiobutton(radioFrame, text="Sign-out", variable=r, value="sign out", background="tomato")

save_button = Button(root, text="Save", command=save)


# Pack stuff
myLabel.pack()
name_scrollbar.pack(side=RIGHT, fill=Y)
name_box.pack()
name_frame.pack()
sign_in_radio.grid(row=0, column=0)
style = Style(root)
sign_out_radio.grid(row=0, column=1)
radioFrame.pack()
save_button.pack()

root.mainloop()

f.close()