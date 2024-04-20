
 
class CircularQueue(object):
    def __init__(self, qSize):
        self.q = [None] * qSize
        self.front = 0
        self.rear = -1
        self.size = 0
        self.max_size = qSize

    def enqueue(self, item):
        if self.is_full():
            raise ValueError("Queue is full.")
        else:
            """ modulo operator allows pointers to wrap around to the beginning of the array once they reach the end. """
            self.rear = (self.rear + 1) % self.max_size
            self.q[self.rear] = item
            self.size += 1
            return True

    def dequeue(self):
        if self.is_empty():
            raise ValueError("Queue is empty.")
        else:
            self.size -= 1
            item = self.q[self.front]
            self.front = (self.front + 1) % self.max_size
            return item

    def is_full(self):
        return self.size == self.max_size
    
    def is_empty(self):
        return self.size == 0

    def show_queue(self):
        return " ".join(str(item) for item in self.q[self.front:self.rear + 1])
