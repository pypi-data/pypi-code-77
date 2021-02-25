from rx.scheduler.eventloop import AsyncIOScheduler
from .task import Task

class Scheduler:
    def __init__(self, loop):
        self.scheduler = AsyncIOScheduler(loop=loop)
        self.loop = loop
        self.tasks = {}

    def taskList(self):
        return self.tasks.keys()

    def addTask(self, fn, name='unnamed', interval=1):
        if name in self.tasks.keys():
            raise AttributeError(f'Task "{name}" is defined already')
        self.tasks[name] = {
            'task': Task(
                fn,
                name=name,
                interval=interval
            ),
            'handler': None
        } 

    def delTask(self, name):
        if name not in self.tasks.keys():
            raise AttributeError(f'There is no "{name}" task defined')
        if self.tasks[name]['handler'] is not None:
            self.tasks[name]['handler'].dispose()
        del(self.tasks[name])

    def runTask(self, name):
        if name not in self.tasks.keys():
            raise AttributeError(f'There is no "{name}" task defined')
        if self.tasks[name]['handler'] is not None:
            raise AttributeError(f'Task "{name}" is running')
        self.tasks[name]['handler'] = self.tasks[name]['task'].run(self.scheduler, self.loop)
           

    def stopTask(self, name):
        if name not in self.tasks.keys():
            raise AttributeError(f'There is no "{name}" task defined')
        if self.tasks[name]['handler'] is None:
            raise AttributeError(f'Task "{name}" is not running')
        self.tasks[name]['handler'].dispose()