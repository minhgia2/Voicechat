import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

# Thiết lập trạng thái trực tuyến, không làm phiền hoặc nghỉ ngơi
status = "online"

# Nhập ID máy chủ và kênh của bạn
GUILD_ID = 1081611251462975528
CHANNEL_ID = 1081611252033388699

# Thiết lập token Discord
usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[LỖI] Vui lòng thêm token vào Secrets.")
    sys.exit()

# Thiết lập header cho các yêu cầu API
headers = {"Authorization": usertoken, "Content-Type": "application/json"}

# Kiểm tra tính hợp lệ của token
validate = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[LỖI] Token của bạn có thể không hợp lệ. Vui lòng kiểm tra lại.")
    sys.exit()

# Lấy thông tin người dùng
userinfo = requests.get('https://discord.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

# Định nghĩa hàm joiner để kết nối với kênh thoại
def joiner(token, status, guild_id, channel_id):
    # Thiết lập kết nối WebSocket
    ws = websocket.WebSocketApp(f"wss://gateway.discord.gg/?v=9&encoding=json",
                              header=headers,
                              on_message=on_message)
    ws.on_open = on_open
    ws.run_forever()

# Định nghĩa hàm xử lý sự kiện khi có tin nhắn mới
def on_message(ws, message):
    # Xử lý các sự kiện và tin nhắn WebSocket
    data = json.loads(message)
    if data.get("op") == 10:
        heartbeat_interval = data["d"]["heartbeat_interval"]
        start_heartbeat(ws, heartbeat_interval)
    elif data.get("op") == 11:
        # Xử lý ACK nhịp tim
        pass
    elif data.get("op") == 0 and data["t"] == "VOICE_STATE_UPDATE":
        # Xử lý cập nhật trạng thái thoại
        voice_state = data["d"]
        if voice_state["channel_id"] == str(CHANNEL_ID):
            # Tham gia kênh thoại
            join_voice_channel(ws, voice_state)
        else:
            # Rời khỏi kênh thoại
            leave_voice_channel(ws, voice_state)

# Định nghĩa hàm để bắt đầu nhịp tim
def start_heartbeat(ws, interval):
    # Gửi nhịp tim để giữ kết nối hoạt động
    def run(*args):
        payload = {"op": 1, "d": None}
        ws.send(json.dumps(payload))

    heartbeat = time.time()
    while True:
        time.sleep(interval / 1000)
        if time.time() - heartbeat > interval / 1000:
            break

    ws.keep_running = False

# Định nghĩa hàm để tham gia kênh thoại
def join_voice_channel(ws, voice_state):
    # Gửi payload cập nhật trạng thái thoại để tham gia kênh
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

# Định nghĩa hàm để rời khỏi kênh thoại
def leave_voice_channel(ws, voice_state):
    # Gửi payload cập nhật trạng thái thoại để rời khỏi kênh
    payload = {
        "op": 4,
        "d": voice_state
    }
    ws.send(json.dumps(payload))

# Định nghĩa hàm để chạy hàm joiner
def run_joiner():
    # Xóa màn hình
    os.system("clear")
    print(f"Đã đăng nhập với tài khoản {username}{discriminator} ({userid}).")
    joiner(usertoken, status, GUILD_ID, CHANNEL_ID)

# Giữ cho dịch vụ hoạt động và chạy hàm joiner
keep_alive()
run_joiner()
