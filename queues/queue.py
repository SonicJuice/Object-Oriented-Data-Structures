

class Queue(object):
    """ constructor method initializes the queue with a given size qSize. It creates a list of Nones of 'q_size' to represent 
    the queue, initialises the front and rear pointers, the size of the queue, and its maximum size.  """
    def __init__(self, q_size):
        self.q = [None] * q_size
        self.front = 0
        self.rear = -1
        self.size = 0
        self.max_size = q_size

    def enqueue(self, item):
        """ adds an element item to the rear, first checking if the queue is full. Otherwise, it increments the rear pointer, 
        assigns the item to the rear of the queue and increments the size of the queue, and returns True. """
        if self.is_full():
            raise ValueError("Queue is full.")
        else:
            self.rear += 1
            self.q[self.rear] = item
            self.size += 1

    def dequeue(self):
        """ removes and returns the element from the front, first checking if the queue is empty. Otherwise, it decrements the size of 
        the queue, retrieves the element from the front of the queue, increments the front pointer, and returns the retrieved 
        element. """
        if self.is_empty():
            raise ValueError("Queue is empty.")
        else:
            self.size -= 1
            item = self.q[self.front]
            self.front += 1
            return item

    def is_full(self):
        return self.size == self.max_size

    def is_empty(self):
        return self.size == 0

    def show_queue(self):
        return " ".join(str(item) for item in self.q[self.front:self.rear + 1])
