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
    sys.exit()

# Get user information
userinfo = requests.get('https://discord.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status, guild_id, channel_id):
    # Establish a WebSocket connection
    ws = websocket.WebSocketApp(f"wss://gateway.discord.gg/?v=9&encoding=json",
                              header=headers,
                              on_message=on_message)
    ws.on_open = on_open
    ws.run_forever()

# ... (rest of the code remains the same)

def run_joiner():
    # Clear the screen
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    joiner(usertoken, status, GUILD_ID, CHANNEL_ID)

# Keep the service alive and run the joiner function
keep_alive()
run_joiner()
