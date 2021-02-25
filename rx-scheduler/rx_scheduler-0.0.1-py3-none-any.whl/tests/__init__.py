import asyncio, logging, unittest
from rx_scheduler import Scheduler, Task

class RxSchedulerTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    async def test_sync(self):
        loop = asyncio.get_event_loop()
        scheduler = Scheduler(loop)

        self.assertRaisesRegex(
            AttributeError,
            'There is no "syncTask" task defined',
            lambda: scheduler.runTask('syncTask')
        )
        self.assertRaisesRegex(
            AttributeError,
            'There is no "syncTask" task defined',
            lambda: scheduler.stopTask('syncTask')
        )
        self.assertRaisesRegex(
            AttributeError,
            'There is no "syncTask" task defined',
            lambda: scheduler.delTask('syncTask')
        )
        
        scheduler.addTask(
            lambda i: logging.debug('sync task output'),
            name = 'syncTask',
            interval = 1
        )

        self.assertTrue('syncTask' in scheduler.taskList())

        self.assertRaisesRegex(
            AttributeError,
            'Task "syncTask" is defined already',
            lambda: scheduler.addTask(
                lambda i: logging.debug('sync task output'),
                name = 'syncTask',
                interval = 1
            )
        )

        self.assertRaisesRegex(
            AttributeError,
            'Task "syncTask" is not running',
            lambda: scheduler.stopTask('syncTask')
        )

        scheduler.runTask('syncTask')
        
        self.assertRaisesRegex(
            AttributeError,
            'Task "syncTask" is running',
            lambda: scheduler.runTask('syncTask')
        )

        await asyncio.sleep(5)
        scheduler.stopTask('syncTask')

        scheduler.delTask('syncTask')
        self.assertFalse('syncTask' in scheduler.taskList())


    async def test_async(self):
        async def async_fn():
            await asyncio.sleep(0.5)
            logging.debug('async task output')

        loop = asyncio.get_event_loop()
        scheduler = Scheduler(loop)

        self.assertRaisesRegex(
            AttributeError,
            'There is no "asyncTask" task defined',
            lambda: scheduler.runTask('asyncTask')
        )
        self.assertRaisesRegex(
            AttributeError,
            'There is no "asyncTask" task defined',
            lambda: scheduler.stopTask('asyncTask')
        )
        self.assertRaisesRegex(
            AttributeError,
            'There is no "asyncTask" task defined',
            lambda: scheduler.delTask('asyncTask')
        )

        scheduler.addTask(
            async_fn,
            name = 'asyncTask',
            interval = 1
        )

        self.assertTrue('asyncTask' in scheduler.taskList())

        self.assertRaisesRegex(
            AttributeError,
            'Task "asyncTask" is defined already',
            lambda: scheduler.addTask(
                async_fn,
                name = 'asyncTask',
                interval = 1
            )
        )

        self.assertRaisesRegex(
            AttributeError,
            'Task "asyncTask" is not running',
            lambda: scheduler.stopTask('asyncTask')
        )

        scheduler.runTask('asyncTask')
        
        self.assertRaisesRegex(
            AttributeError,
            'Task "asyncTask" is running',
            lambda: scheduler.runTask('asyncTask')
        )

        await asyncio.sleep(5)
        scheduler.stopTask('asyncTask')

        scheduler.delTask('asyncTask')
        self.assertFalse('asyncTask' in scheduler.taskList())
