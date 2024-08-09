import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive, is_port_open, scan_ports

status = "online"  # online/dnd/idle

GUILD_ID = 1081611251462975528
CHANNEL_ID = 1081611252033388699
SELF_MUTE = True
SELF_DEAF = False

usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-type": "application/json"}

validate = requests.get('https://canary.discord.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get('https://canary.discord.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status):
    # Your code for joining voice channels and handling WebSocket connection
    pass

def run_joiner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, status)
        time.sleep(30)

# Scan for open ports and keep the service alive
keep_alive()

# Run the joiner function
run_joiner()
