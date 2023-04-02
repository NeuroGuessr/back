import asyncio

class Timer:
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def remind(self, seconds: int, message: dict):
        asyncio.create_task(self.sleep_and_send(seconds, message))

    async def sleep_and_send(self, seconds: int, message: dict):
        await asyncio.sleep(seconds)
        await self.queue.put(('TIMER', message ))