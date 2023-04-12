class Song:
    def __init__(self, link, title):
        self.link = link
        self.title = title
    
class Queue:
    def __init__(self):
        self.q:list[Song] = []
    
    def append(self, link, title):
        self.q.append(Song(link, title))

