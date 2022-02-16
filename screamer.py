import time

import requests
import json
import asyncio
from gtts import gTTS
from playsound import playsound
import os

running = True


async def screamer():
    og = retrieve_door_user(channelid="862494771615891476")
    while running:
        if og != retrieve_door_user(channelid="862494771615891476"):
            print(f'{retrieve_door_user(channelid="862494771615891476")} is a screamer')
            og = retrieve_door_user(channelid="862494771615891476")


async def tkloop():
    tkintermainloop = 1


async def main():
    await asyncio.gather(screamer(), tkloop())


def retrieve_door_user(channelid):
    headers = {
        'authorization': "MzA2NTM4NzAzNjg0MjM5MzYw.YZ7nvA.pCNYSWGszqKWmcbz3LVBhgFcRgo",
    }
    r = requests.get(f"https://discord.com/api/v9/channels/{channelid}/messages", headers=headers)
    jsonn = json.loads(r.text)
    for message in jsonn:
        if ("<@&862495078727680001>" in message["content"]):
            return message["author"]["username"]


# asyncio.run(main())

scream = gTTS(text="Emo woofy", lang="en", slow=False)
scream.save("scream.mp3")
time.sleep(1.5)
# os.system("start scream.mp3")
playsound("scream.mp3")
try:
    os.remove("scream.mp3")
except:
    pass
