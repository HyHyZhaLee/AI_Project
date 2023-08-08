from os.path import dirname, join
from PIL import ImageGrab

from app import MainApp
from kivy.core.window import Window

# Lấy kích thước màn hình
resolution = ImageGrab.grab().size

# Đặt cửa sổ ứng dụng nằm ở giữa màn hình
Window.top = (resolution[1] - 720) // 2
Window.left = (resolution[0] - 1280) // 2

# Đặt kích thước của cửa sổ ứng dụng
Window.size = (1280, 720)
# Tạo và chạy ứng dụng chính
MainApp().run()
