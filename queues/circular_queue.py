

class CircularQueue:
    def __init__(self, capacity):
        self.queue = [None for _ in range(capacity)]
        """ current head and tail pointers, and the number of enqueued items. """
        self.head = self.tail = self.size = 0
        self.capacity = capacity

    def qsize(self):
        return self.size
    
    def empty(self):
        return self.qsize() == 0
    
    def full(self):
        return self.qsize() == self.capacity
    
    def enqueue(self, item):
        if self.full():
            raise ValueError("Queue is full")
        """ insert an item at the tail index, before incrementing it modulo the capacity (to ensure 
        that when the pointer wraps around to the beginning of the array upon reaching the end, 
        reusing the space released by dequeuing elements), as well as the size. """
        self.queue[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        if self.empty():
            raise ValueError("Queue is empty")
        """ remove and return the item at the head index, before incrementing it modulo the 
        capacity, as well as the size. """
        item = self.queue[self.head]
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item
