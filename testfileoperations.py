import pandas as pd
from datetime import date
from datetime import time



f = pd.read_csv("RoboticsHourLog.csv")

# print the time
print(current_time)

# writing into the file
f.to_csv("RoboticsHourLog.csv", index=False)

print(f)
