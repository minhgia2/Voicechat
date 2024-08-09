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

# ... (mã còn lại vẫn giữ nguyên)

# Định nghĩa hàm run_joiner để chạy hàm joiner
def run_joiner():
    # Xóa màn hình
    os.system("clear")
    print(f"Đã đăng nhập với tài khoản {username}{discriminator} ({userid}).")
    joiner(usertoken, status, GUILD_ID, CHANNEL_ID)

# Giữ cho dịch vụ hoạt động và chạy hàm joiner
keep_alive()
run_joiner()
