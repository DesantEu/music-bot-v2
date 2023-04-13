from datetime import datetime
import asyncio
import discord
from songQueue import Queue
import player

class Instance:
    def __init__(self, gid:int, prefix:str):
        self.guildid:int = gid
        self.prefix:str = prefix
        self.queue = Queue()
        self.skipSkip = False
        self.song_start_time = datetime.now()
        self.pause_time = datetime.now()
        self.pos = 0
        self.current = -1
        self.volume = 1.0
        self.isPlaying = False
        self.isStopped = True
        self.isPaused = False
        self.vc:discord.VoiceClient

        asyncio.Task(self.watcher())

    async def update_queue(self):
        # try:
        #     self.vc
        #     
        #     # return if queue empty
        #     if self.queue.len() < 1:
        #         return
        #     # otherwise start playing something
        #     if self.isStopped:
        #         self.current = 0
        #         await player.resume(self)
        #
        #     
        #
        # except:
        #     # stop if nothing is to be played
        #     # if self.isPlaying or self.isPaused:
        #     #     await player.stop(self)
        #     pass
        #
        #

        pass

    def after_song(self, error):
        if error:
            return

        # avoid recursion when skipping
        if self.skipSkip:
            self.skipSkip = False
            return
        print('after_song is called')
        player.skip(self, afterSong=True)
        pass


    async def check_disconnect(self):
        pass

    async def watcher(self):
        await self.update_queue()
        await self.check_disconnect()

    def hasVC(self) -> bool:
        try:
            self.vc
            return True
        except:
            return False

