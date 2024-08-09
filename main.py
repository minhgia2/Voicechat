import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = "online"  # online/dnd/idle

GUILD_ID = 1081611251462975528
CHANNEL_ID = 1081611252033388699
SELF_MUTE = True
SELF_DEAF = False

usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status):
    ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json",
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()

def run_joiner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, status)
        time.sleep(30)

def on_open(ws):
    print("WebSocket connection opened")

def on_message(ws, message):
    # Process incoming messages
    pass

def on_error(ws, error):
    # Handle WebSocket errors
    print("WebSocket Error:", error)

def on_close(ws):
    # Handle WebSocket connection closure
    print("WebSocket Connection Closed")

keep_alive()
run_joiner()
