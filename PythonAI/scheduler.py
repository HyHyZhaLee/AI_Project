from tasks import *
class Task:
    def __init__(self, task_func, delay, period):
        self.task_func = task_func
        self.delay = delay
        self.period = period
        self.run_me = 0

class Scheduler:
    TICK = 1000
    MAX_TASKS = 40

    def __init__(self):
        self.tasks = []

    def Init(self):
        task1 = Task1() # Uploading image and AI_Result
        self.add_task(task1.run, 3000, 100)
        self.add_task(task1.publishResult, 3000, 5000)
        self.add_task(task1.publishImage, 3000, 100)

    def add_task(self, task_func, delay, period):
        if len(self.tasks) < self.MAX_TASKS:
            task = Task(task_func, delay / self.TICK, period / self.TICK)
            self.tasks.append(task)
        else:
            print("Scheduler tasks are full!!!")

    def update(self):
        for task in self.tasks:
            if task.delay > 0:
                task.delay -= 1
            else:
                task.delay = task.period
                task.run_me += 1

    def delete_task(self, task):
        print("1 task have been deleted!")
        self.tasks.remove(task)

    def dispatch_tasks(self):
        for task in self.tasks:
            if task.run_me > 0:
                task.task_func()
                task.run_me -= 1
                if task.period <= 0:
                    self.delete_task(task)