import cv2
import time
import requests
# Địa chỉ IP và cổng của ESP32-CAM
ip_address = '192.168.2.10'
port = 80

# Đường dẫn streaming cụ thể
stream_url = 'http://192.168.220.199:81/stream'

# Tạo một đối tượng VideoCapture với URL streaming
cap = cv2.VideoCapture(stream_url)

# Kiểm tra xem VideoCapture đã mở thành công hay không
if not cap.isOpened():
    print('Không thể kết nối đến ESP32-CAM.')
    exit()
def adjust_led_intensity(intensity):
    # Địa chỉ IP của ESP32-CAM
    ip_address = '192.168.220.199'

    # Tạo URL điều khiển LED với giá trị độ sáng mới
    url = 'http://{}/control?var=led_intensity&val={}'.format(ip_address, intensity)

    # Gửi yêu cầu HTTP GET để điều chỉnh độ sáng LED
    response = requests.get(url)

    # Kiểm tra xem yêu cầu có thành công hay không
    if response.status_code == 200:
        print('Đã điều chỉnh độ sáng LED thành công.')
    else:
        print('Không thể điều chỉnh độ sáng LED.')

# Sử dụng hàm để điều chỉnh độ sáng LED
intensity_value = 128  # Giá trị độ sáng mong muốn (từ 0 đến 255)
adjust_led_intensity(intensity_value)
val = 0

# Đọc và hiển thị các khung hình từ ESP32-CAM
while True:
    ret, frame = cap.read()

    # Kiểm tra xem việc đọc khung hình thành công hay không
    if not ret:
        print('Không thể đọc khung hình.')
        break

    # Hiển thị khung hình
    cv2.imshow('ESP32-CAM Stream', frame)
    val += 50
    if val >= 225:
        val = 0
    adjust_led_intensity(val)
    time.sleep(3)

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()

