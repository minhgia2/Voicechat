import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = "online"  # online/dnd/idle

# Your server and channel IDs
GUILD_ID = ADD_YOUR_SERVER_ID_HERE
CHANNEL_ID = ADD_YOUR_CHANNEL_ID_HERE

# Set the Discord token
usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

# Validate the token
validate = requests.get('https://canary.discord.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

# Get user information
userinfo = requests.get('https://canary.discord.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status):
    # Your code for joining voice channels and handling WebSocket connection
    pass

def run_joiner():
    # Clear the screen
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, status)
        time.sleep(30)

# Keep the service alive and run the joiner function
keep_alive()
run_joiner()
