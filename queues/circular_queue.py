

class CircularQueue:
    def __init__(self, capacity):
        self.queue = [None for _ in range(capacity)]
        self.front = 0
        self.rear = 0
        self.size = 0
        self.capacity = capacity
    
    def enqueue(self, item):
        if self.full():
            raise ValueError("Queue is full")
        self.queue[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        if self.empty():
            raise ValueError("Queue is empty")
        item = self.queue[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item
    
    def full(self):
        return self.capacity == self.size

    def empty(self):
        return self.size == 0
