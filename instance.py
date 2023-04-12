from datetime import datetime
class Instance:

    def __init__(self, gid, prefix:str):
        self.guildid = gid
        self.prefix = prefix
        self.queue = []
        self.link_queue = []
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
        self.messages = []

