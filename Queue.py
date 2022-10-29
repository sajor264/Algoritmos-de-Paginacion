class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def queue(self, item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop()

    def len(self):
        return len(self.items)

    def clear(self):
        self.items = []