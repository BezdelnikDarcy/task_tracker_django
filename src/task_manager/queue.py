
class EmptyQueueError(Exception):
    pass


class UniqueQueue:
    LIFO = "LIFO"
    FIFO = "FIFO"
    STRATEGIES = [LIFO, FIFO]
    def __init__(self, strategy: str = LIFO):
        self.storage = []
        self.strategy = strategy
        if self.strategy not in self.STRATEGIES:
            raise TypeError

    def add(self, item):
        if self.strategy == self.LIFO:
            if item not in self.storage:
                self.storage.append(item)


    def remove(self):
        if self.strategy == self.LIFO:
            if not self.storage:
                raise EmptyQueueError
            return self.storage.pop()

    def get_length_of_queue(self):
        if self.strategy == self.LIFO:
            return len(self.storage)

    def get_last_item(self):
        if self.strategy == self.LIFO:
            if not self.storage:
                raise EmptyQueueError
            return self.storage[-1]
