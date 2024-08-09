import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = "online"  # online/dnd/idle

# Your server and channel IDs
GUILD_ID = 1081611251462975528
CHANNEL_ID = 1081611252033388699

# Set the Discord token
usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

# Validate the token
validate = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sysMultiplier = 1
    sys.exit()

# Get user information
userinfo = requests.get('https://discord.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status, guild_id, channel_id):
    # Establish a WebSocket connection
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://gateway.discord.gg/?v=9&encoding=json",
                              header=headers,
                              on_message=on_message)
    ws.on_open = on_open
    ws.run_forever()

def on_open(ws):
    # Send the identify payload to join the voice channel
    payload = {
        "op": 2,
        "d": {
            "token": usertoken,
            "properties": {"$os": "linux", "$browser": "python"},
            "compress": False,
            "large_threshold": 250,
            "presence": {"status": status},
            "guild_id": guild_id,
            "intent": 513
        }
    }
    ws.send(json.dumps(payload))

def on_message(ws, message):
    # Handle WebSocket messages and events
    data = json.loads(message)
    if data.get("op") == 10:
        heartbeat_interval = data["d"]["heartbeat_interval"]
        start_heartbeat(ws, heartbeat_interval)
    elif data.get("op") == 11:
        # Handle the heartbeat ACK
        pass
    elif data.get("op") == 0 and data["t"] == "VOICE_STATE_UPDATE":
        # Handle voice state updates
        voice_state = data["d"]
        if voice_state["channel_id"] == str(CHANNEL_ID):
            # Join the voice channel
            join_voice_channel(ws, voice_state)
        else:
            # Leave the voice channel
            leave_voice_channel(ws, voice_state)

def start_heartbeat(ws, interval):
    # Send heartbeat to keep the connection alive
    def run(*args):
        payload = {"op": 1, "d": None}
        ws.send(json.dumps(payload))

    heartbeat = time.time()
    while True:
        time.sleep(interval / 1000)
        if time.time() - heartbeat > interval / 1000:
            break

    ws.keep_running = False

def join_voice_channel(ws, voice_state):
    # Send the voice server update payload
    payload = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "self_mute": False,
            "self_deaf": False
        }
    }
    ws.send(json.dumps(payload))

def leave_voice_channel(ws, voice_state):
    # Send the voice state update payload to leave the voice channel
    payload = {
        "op": 4,
        "d": voice_state
    }
    ws.send(json.dumps(payload))

def run_joiner():
    # Clear the screen
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    joiner(usertoken, status, GUILD_ID, CHANNEL_ID)

# Keep the service alive and run the joiner function
keep_alive()
run_joiner()
