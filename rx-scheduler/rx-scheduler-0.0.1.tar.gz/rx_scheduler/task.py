import rx, logging, asyncio
import rx.operators as ops

class Observer:
    def __init__(self,
        on_next=lambda i: None,
        on_error=lambda i: None,
        on_completed=lambda i: None):
        self.on_next = on_next
        self.on_error = on_error
        self.on_completed = on_completed


class Task:
    def __init__(self, fn, name='unnamed', interval = 1.0):
        self.name = name
        self.interval = interval
        self.fn = fn
    
    def run(self, scheduler, loop):
        if asyncio.iscoroutinefunction(self.fn):
            return (
                rx
                .interval(self.interval)
                .pipe(
                    ops.do(Observer(
                        on_next=lambda i: logging.debug(f'{self.name} is runnnig {i} time')
                    )),
                    ops.map(lambda i: rx.from_future(asyncio.create_task(self.fn()))),
                    ops.merge_all(),
                )
                .subscribe(scheduler=scheduler)
            )
        else:
            return (
                rx
                .interval(self.interval)
                .pipe(
                    ops.do(Observer(
                        on_next=lambda i: logging.debug(f'{self.name} is runnnig {i} time')
                    )),
                )
                .subscribe(
                    self.fn,
                    scheduler=scheduler
                )
            )