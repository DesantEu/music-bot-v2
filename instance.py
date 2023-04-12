from datetime import datetime
import asyncio

class Instance:

    def __init__(self, gid:int, prefix:str):
        self.guildid:int = gid
        self.prefix:str = prefix
        self.queue:list[str] = []
        self.link_queue:list[str] = []
        self.song_start_time = datetime.now()
        self.pause_time = datetime.now()
        self.song_len = 0
        self.pos = 0
        self.total_songs = 0
        self.current = -1
        self.volume = 1.0
        self.isPlaying = False
        self.isStopped = True
        self.isPaused = False

        task = asyncio.Task(self.watcher())

    async def manage_queue(self):
        pass

    async def check_disconnect(self):
        pass

    async def watcher(self):
        await self.manage_queue()
        await self.check_disconnect()

