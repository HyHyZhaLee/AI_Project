#Begin import
import time
import random
from scheduler import *
from tasks import*
#End import

#Setting up
#Connect to adafruit
Adafruit_connect()

#Set up scheduler
task1 = Task1()
scheduler = Scheduler()
scheduler.add_task(task1.Task1_Run, 5000, 5000)

next_time = time.time() + 1  # Thời điểm bắt đầu của chu kỳ tiếp theo

# Wait until connection is established

while True:
    current_time = time.time()
    if current_time >= next_time:
        # TODO
        scheduler.update()
        scheduler.dispatch_tasks()
        next_time += 1  # Cập nhật thời điểm bắt đầu của chu kỳ tiếp theo
    time.sleep(0.01)  # Ngủ một thời gian rất nhỏ để tránh sử dụng CPU quá nhiều