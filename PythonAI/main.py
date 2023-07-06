# Begin import
import time
from scheduler import *
# End import

# Link to adafruit: https://io.adafruit.com/AI_ProjectHGL/dashboards/ai-hgl

# Setting up
# Connect to adafruit
Adafruit_connect()

# Set up scheduler
scheduler = Scheduler()

task1 = Task1("192.168.50.120") # Uploading image and AI_Result
scheduler.add_task(task1.run, 3000, 100)
scheduler.add_task(task1.publishResult, 3000, 5000)
scheduler.add_task(task1.publishImage, 3000, 100)

next_time = time.time() + 1  # The start of the next cycle


while True:
    current_time = time.time()
    if current_time >= next_time:
        # TODO
        scheduler.update()
        scheduler.dispatch_tasks()
        next_time += 1  # Update the start of the next cycle
    time.sleep(0.01)  # Sleep a very small time to avoid excessive CPU usage