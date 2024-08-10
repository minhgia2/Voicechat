import os
import sys
import json
import time
import requests
import websockets
import asyncio
from keep_alive import keep_alive

status = "idle" #online/dnd/idle

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

async def joiner(token, status):
    try:
        async with websockets.connect('wss://gateway.discord.gg/?v=9&encoding=json') as ws:
            start = json.loads(await ws.recv())
            heartbeat = start['d']['heartbeat_interval']
            auth = {"op": 2,"d": {"token": token,"properties": {"$os": "Windows 10","$browser": "Google Chrome","$device": "Windows"},"presence": {"status": status,"afk": False}},"s": None,"t": None}
            vc = {"op": 4,"d": {"guild_id": GUILD_ID,"channel_id": CHANNEL_ID,"self_mute": SELF_MUTE,"self_deaf": SELF_DEAF}}
            await ws.send(json.dumps(auth))
            await ws.send(json.dumps(vc))

            # Convert heartbeat from milliseconds to seconds
            await asyncio.sleep(heartbeat / 1000) 
            await ws.send(json.dumps({"op": 1,"d": None}))
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed: {e}")
    except Exception as e:
        print(f"Error in joiner(): {e}")

async def run_joiner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        try:
            await joiner(usertoken, status)
        except Exception as e:
            print(f"Error in run_joiner(): {e}")
        await asyncio.sleep(30)

try:
    asyncio.run(run_joiner())
except Exception as e:
    print(f"Error running bot: {e}")

keep_alive()
