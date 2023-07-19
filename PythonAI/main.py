# Begin import
import time
from scheduler import *
from PrivateTask.task1 import *
from PrivateTask.task2 import *
# End import

# Link to adafruit: https://io.adafruit.com/AI_ProjectHGL/dashboards/ai-hgl

# Setting up
# Setup camera
camera = Camera('192.168.1.35')

# Set up scheduler
scheduler = Scheduler()

# Adding task
task1 = Task1() # Connect to adafruit task (1 shot task)
task2 = Task2(camera) # Uploading image and AI_Result with IP task

scheduler.add_task(task1.run,0,0)
scheduler.add_task(task2.run, 3000, 100) # Camera delay for 3s and run checking every 100ms
scheduler.add_task(task2.publishResult, 3000, 5000)  # Delay for 3s and Publish AI result with confident score every 5s
scheduler.add_task(task2.publishImage, 3000, 5000) # Delay for 3s and Publish Image every 100ms

# Clock cycle define for time.sleep more effective
next_time = time.time() + 1  # The next cycle

# Super loop program
while True:
    current_time = time.time()  # This time cycle
    if current_time >= next_time:
        # TODO
        scheduler.update() # scheduler timer run
        scheduler.dispatch_tasks()  # dispatch tasks that on run flag
        next_time += 1  # Update the start of the next cycle
    time.sleep(0.01)  # Sleep a very small time to avoid excessive CPU usage