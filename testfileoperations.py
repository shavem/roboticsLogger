import pandas as pd
from datetime import datetime
import time


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


df = pd.read_csv("RoboticsHourLog.csv")
df.to_csv("RoboticsHourLog.csv", index=False)

# print the time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

if not current_date in df.columns:
    df[current_date] = ""

# Try signing in
df.loc[df.index[df["Name"] == "Uddish Sood"].tolist()[0], current_date] = now.strftime("%H:%M:%S")

time.sleep(5)

# Try signing out
now = datetime.now()
hours_to_add = time_difference(df.loc[df.index[df["Name"] == "Uddish Sood"].tolist()[0], current_date], now.strftime("%H:%M:%S"))
df.loc[df.index[df["Name"] == "Uddish Sood"].tolist()[0], current_date] += f" - {now.strftime('%H:%M:%S')}"
df.loc[df.index[df["Name"] == "Uddish Sood"].tolist()[0], "Hours"] = seconds_to_time(time_to_seconds(df.loc[df.index[df["Name"] == "Uddish Sood"].tolist()[0], "Hours"]) + hours_to_add)


# CLosing operations
# Order the rows by the number of hours and update members file
df = df.sort_values(by=["Hours"], ascending=False)
# for row in df.iterrows():
#     f.write(row[1]["Name"] + "\n")
# writing into the file
df.to_csv("RoboticsHourLog.csv", index=False)

print(df)
