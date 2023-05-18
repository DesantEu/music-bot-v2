from datetime import datetime
import discord
from songQueue import Queue
import player
import dcHandler as dc
class Instance:
    def __init__(self, gid:int, prefix:str):
        self.guildid:int = gid
        self.prefix:str = prefix
        self.queue = Queue()
        self.queue_messages:list[int] = []
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

    async def update_queue(self):
        # delete old queue messages
        max_messages = 5
        if len(self.queue_messages) > max_messages:
            while True:
                # self.queue_messages.pop(list(self.queue_messages.items())[0][0])
                self.queue_messages.pop(0)
                if len(self.queue_messages) <= max_messages:
                    break

        # update queue messages
        for i in self.queue_messages:
            # await dc.edit_status(i, self.queue_messages[i], self.queue)
            await dc.edit_long_content(i, [[self.queue.index(i), i.title] for i in self.queue])

    def after_song(self, error):
        if error:
            return

        # avoid recursion when skipping
        if self.skipSkip:
            self.skipSkip = False
            return
        player.skip(self, afterSong=True)
        pass


    async def on_disconnect(self):
        player.stop(self)
        await dc.leave(self)
        print('got kicked, leaving')


    def hasVC(self) -> bool:
        try:
            self.vc
            return True
        except:
            return False

