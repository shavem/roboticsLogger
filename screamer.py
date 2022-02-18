import time
import requests
import json
import threading
from gtts import gTTS
from playsound import playsound
import os


# channelid = "862494771615891476"  # Door-channel
channelid = "940177279953301524"  # Dev-testing


# def screamer(channelid, interval):
#     og = retrieve_door_user(channelid)
#     while True:
#         time.sleep(interval)
#         user = retrieve_door_user(channelid)
#         if og != user:
#             print(f'{user} is a screamer')
#             og = user



def retrieve_door_user(channelid):
    headers = {
        # 'authorization': "MzA2NTM4NzAzNjg0MjM5MzYw.YZ7nvA.pCNYSWGszqKWmcbz3LVBhgFcRgo",
        'authorization': "mfa.cS-xvOm-L7m-KeOxNBOHrFplEvCS6YDhg6-h5rGbRKiAERAJ24EibBroAVxlqTZIRDldeLwlJ9-gTUThCy7g",
    }
    r = requests.get(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers)
    jsonn = json.loads(r.text)
    for message in jsonn:
        # if ("<@&862495078727680001>" in message["content"]):
        #     return message["author"]["username"]
        if ("hi" in message["content"]):
            # return message["author"]["username"]
            print(message["author"]["username"])



# thread = threading.Thread(target=screamer, args=(channelid, 5))
# thread.start()
# time.sleep(60)
# if thread.is_alive():
#     thread.join()
#     print("Thread is dead")

print(retrieve_door_user(channelid))

# scream = gTTS(text="lewis", lang="en", slow=False)
# await scream.save("scream.mp3")
# # time.sleep(1.5)
# playsound("scream.mp3")
# try:
#     os.remove("scream.mp3")
# except:
#     pass
