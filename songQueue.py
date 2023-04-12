class Song:
    def __init__(self, link, title):
        self.link = link
        self.title = title
        self.length = 0 # TODO
    
class Queue:
    def __init__(self):
        self.q:list[Song] = []

    def __getitem__(self, key):
        return self.q[key]
    
    def append(self, link, title):
        self.q.append(Song(link, title))

    def len(self):
        return len(self.q)

    def clear(self):
        self.q = []
