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

    def pop(self, index):
        if index.startswith('-') or not index.isdigit() or self.len() == 0 or index == '':
            return False

        index = int(index)
        if index < 1 or index > self.len():
            return False

        self.q.pop(index - 1)
        return True
            

    def len(self):
        return len(self.q)

    def clear(self):
        self.q = []

    def __str__(self) -> str:
        return '\n'.join([f'{self.q.index(i) + 1}. ' + i.title for i in self.q])

    def toStrWithCurrent(self, current) -> str:
        return '\n'.join([f"{'> ' if current == self.q.index(i) else '  '}" + f'{self.q.index(i) + 1}. ' + i.title for i in self.q])

