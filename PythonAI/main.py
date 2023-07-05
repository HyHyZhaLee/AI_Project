# Begin import
import time
from scheduler import *
from tasks import*
# End import

# Link to adafruit: https://io.adafruit.com/AI_ProjectHGL/dashboards/ai-hgl

# Setting up
# Connect to adafruit
Adafruit_connect()

# Set up scheduler
task1 = Task1() # Uploading image
task2 = Task2() # Publish AI result
scheduler = Scheduler()

scheduler.add_task(task1.run, 3000, 1000)
scheduler.add_task(task2.run, 3000, 5000)

next_time = time.time() + 1  # The start of the next cycle


while True:
    current_time = time.time()
    if current_time >= next_time:
        # TODO
        scheduler.update()
        scheduler.dispatch_tasks()
        next_time += 1  # Update the start of the next cycle
    time.sleep(0.01)  # Sleep a very small time to avoid excessive CPU usage