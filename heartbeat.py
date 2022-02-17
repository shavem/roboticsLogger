import websocket
import json
import threading
import time

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print("Beginning heartbeat ... THUMP THUMP THUMP")
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")


ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
event = receive_json_response(ws)

heartbeat_interval = event["d"]["heartbeat_interval"] / 1000
thread = threading.Thread(target=heartbeat, args=(heartbeat_interval, ws))
thread.start()
token = "mfa.cS-xvOm-L7m-KeOxNBOHrFplEvCS6YDhg6-h5rGbRKiAERAJ24EibBroAVxlqTZIRDldeLwlJ9-gTUThCy7g"
payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc"
        }
    }
}


while True:
    event = receive_json_response(ws)

    try:
        print(f"{event['d']['author']['username']}: {event['d']['content']}")
        op_code = event("op")
        if op_code == 11:
            print("heartbeat received")
    except:
        pass