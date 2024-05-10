class CircularQueue:
    def __init__(self, maxsize):
        self.queue = [None for _ in range(maxsize)]
        """ current front and rear pointers, and the number of enqueued items. """
        self.front = 0
        self.rear = -1
        self.size = 0
        self.maxsize = maxsize

    def enqueue(self, item):
        if self.full():
            raise ValueError("Queue is full")
        """ insert an item at the rear index, before incrementing it modulo the maxsize (to ensure 
        that when the pointer wraps around to the beginning of the array upon reaching the end, 
        reusing the space released by dequeuing elements), as well as the size. """
        self.rear = (self.rear + 1) % self.maxsize
        self.size += 1
        self.queue[self.rear] = item

    def dequeue(self):
        if self.empty():
            raise ValueError("Queue is empty")
        """ remove and return the item at the front index, before incrementing it modulo the 
        maxsize, as well as the size. """
        item = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.maxsize
        self.size -= 1
        return item

    def full(self):
        return self.size == self.maxsize

    def empty(self):
        return self.size == 0

    def qsize(self):
        return self.size
