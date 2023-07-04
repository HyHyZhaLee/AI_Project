class Task:
    def __init__(self, task_func, delay, period, run_me=0):
        self.task_func = task_func
        self.delay = delay
        self.period = period
        self.run_me = run_me

class Scheduler:
    TICK = 100
    MAX_TASKS = 40

    def __init__(self):
        self.tasks = []

    def add_task(self, task_func, delay, period, run_me=0):
        if len(self.tasks) < self.MAX_TASKS:
            task = Task(task_func, delay / self.TICK, period / self.TICK, run_me)
            self.tasks.append(task)
        else:
            print("Scheduler tasks are full!!!")

    def update(self):
        for task in self.tasks:
            if task.delay > 0:
                task.delay -= 1
            else:
                task.delay = task.period

    def delete_task(self, task):
        print("1 task have been deleted")
        self.tasks.remove(task)

    def dispatch_tasks(self):
        for task in self.tasks:
            task.task_func()
            if task.run_me > 0:
                task.run_me -= 1
                if task.run_me <= 0:
                    self.delete_task(task)