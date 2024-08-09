import sys
import signal
import atexit
import logging
import threading

# Thiết lập logger
logger = logging.getLogger(__name__)

# Thiết lập thời gian mặc định là 3600 giây (1 giờ)
DEFAULT_TIMEOUT = 3600

# Biến toàn cục để theo dõi bộ hẹn giờ giữ hoạt động
global keep_alive_timer

# Định nghĩa hàm giữ hoạt động
def keep_alive(url=None, path="/", port=80, timeout=DEFAULT_TIMEOUT):
    """
    Giữ cho dịch vụ hoạt động bằng cách gửi yêu cầu GET đến URL chỉ định theo khoảng thời gian đều đặn.

    Tham số:
        url (str): URL để gửi yêu cầu giữ hoạt động.
        path (str): Đường dẫn để thêm vào URL.
        port (int): Số cổng để sử dụng cho yêu cầu.
        timeout (int): Khoảng thời gian giữa các yêu cầu giữ hoạt động (tính bằng giây).
    """
    # Biến toàn cục
    global keep_alive_timer

    # Kiểm tra giá trị thời gian hết hạn
    if timeout <= 0:
        logger.warning("Giá trị thời gian hết hạn phải lớn hơn 0. Sử dụng giá trị mặc định.")
        timeout = DEFAULT_TIMEOUT

    # Định nghĩa header cho yêu cầu
    headers = {
        "User-Agent": "Keep-Alive/1.0",
        "Content-type": "application/json",
    }

    # Định nghĩa dữ liệu cho yêu cầu
    data = {"status": "online"}

    # Định nghĩa phương thức yêu cầu
    method = "GET"

    # Định nghĩa hàm yêu cầu
    def request():
        try:
            response = requests.request(method, url + path, headers=headers, data=json.dumps(data))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Không thể gửi yêu cầu giữ hoạt động: {e}")

    # Định nghĩa hàm giữ hoạt động
    def keep_alive_func():
        global keep_alive_timer
        while True:
            try:
                request()
            except Exception as e:
                logger.error(f"Yêu cầu giữ hoạt động thất bại: {e}")
            finally:
                keep_alive_timer = threading.Timer(timeout, keep_alive_func)
                keep_alive_timer.start()

    # Đăng ký hàm giữ hoạt động để chạy khi thoát
    atexit.register(keep_alive_func)

    # Bắt đầu hàm giữ hoạt động
    keep_alive_func()

# Định nghĩa hàm để dừng bộ hẹn giờ giữ hoạt động
def stop_keep_alive():
    """
    Dừng bộ hẹn giờ và yêu cầu giữ hoạt động.
    """
    global keep_alive_timer
    if keep_alive_timer:
        keep_alive_timer.cancel()
        keep_alive_timer = None

# Đăng ký xử lý tín hiệu để dừng bộ hẹn giờ giữ hoạt động khi quá trình nhận được tín hiệu SIGTERM
def signal_handler(sig, frame):
    stop_keep_alive()
    sys.exit(0)

# Đăng ký xử lý tín hiệu SIGTERM
signal.signal(signal.SIGTERM, signal_handler)
