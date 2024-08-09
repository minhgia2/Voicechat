import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive, is_port_open, scan_ports
import platform  # Import the platform module

status = "online"  # online/dnd/idle

# Your Discord token
DISCORD_TOKEN = "NDM5NzM1NjU5OTQzNTU5MTY5.GKL6dj.usVOga-Wp7CD_goIPd_UHpZBhrUnkkhMnx8kt4"

GUILD_ID = 1081611251462975528
CHANNEL_ID = 1081611252033388699
SELF_MUTE = True
SELF_DEAF = False

# Set the Discord token
usertoken = DISCORD_TOKEN

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

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
    # Clear the screen
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, status)
        time.sleep(30)

# Scan for open ports and keep the service alive
keep_alive()

# Run the joiner function
run_joiner()
