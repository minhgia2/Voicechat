import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

# Set the online, do not disturb, or idle status
status = "online"

# Your server and channel IDs
GUILD_ID = 1081611251462975528
CHANNEL_ID = 1081611252033388699

# Set the Discord token
usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

# Set the headers for API requests
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

# Define the joiner function to connect to the voice channel
def joiner(token, status, guild_id, channel_id):
    # Establish a WebSocket connection
    environ = {"HTTP_AUTHORIZATION": token}
    socket = None
    rfile = None
    ws = websocket.WebSocket(environ, socket, rfile)

    # Define the on_open function to handle the WebSocket connection opening
    def on_open(ws):
        # Send the authentication payload
        payload = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {"$os": "linux", "$browser": "python"},
                "compress": False,
                "large_threshold": 250,
                "presence": {"status": status},
                "guild_id": guild_id
            }
        }
        ws.send(json.dumps(payload))

    # Define the on_message function to handle new messages
    def on_message(ws, message):
        # Handle WebSocket events and messages
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

    # Define the on_error function to handle WebSocket errors
    def on_error(ws, error):
        print(f"WebSocket Error: {error}")

    # Define the on_close function to handle the WebSocket connection closing
    def on_close(ws):
        print("WebSocket connection closed")

    # Set the WebSocket event handlers
    ws.on_open = on_open
    ws.on_message = on_message
    ws.on_error = on_error
    ws.on_close = on_close

    # Run the WebSocket in an infinite loop
    while True:
        try:
            ws.run_forever()
        except Exception as e:
            print(f"WebSocket Error: {e}")
            break

    # Close the WebSocket connection
    ws.close()

# Define the run_joiner function to run the joiner function
def run_joiner():
    # Clear the screen
    os.system("clear")
    print(f"Logged in as {username}{discriminator} ({userid}).")
    joiner(usertoken, status, GUILD_ID, CHANNEL_ID)

# Keep the service alive and run the joiner function
keep_alive()
run_joiner()
