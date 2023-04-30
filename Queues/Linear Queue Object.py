

class LinearQueue(object):
    """ constructor method initializes the queue with a given size qSize. It creates a list of Nones of 'q_size' to represent the queue, 
    initialises the front and rear pointers, the size of the queue, and its maximum size.  """
    def __init__(self, q_size):
        self.__q = [None] * q_size
        self.__front = 0
        self.__rear = -1
        self.__size = 0
        self.__max_size = q_size

    def enQueue(self, item):
        """ adds an element item to the rear, first checking if the queue is full. Otherwise, it increments the rear pointer, 
        assigns the item to the rear of the queue and increments the size of the queue, and returns True. """
        if self.isFull():
            raise ValueError("Queue is full.")
        else:
            self.__rear += 1
            self.__q[self.__rear] = item
            self.__size += 1

    def deQueue(self):
        """ removes and returns the element from the front, first checking if the queue is empty. Otherwise, it decrements the size of the queue, 
        retrieves the element from the front of the queue, increments the front pointer, and returns the retrieved element. """
        if self.isEmpty():
            raise ValueError("Queue is empty.")
        else:
            self.__size -= 1
            item = self.__q[self.__front]
            self.__front += 1
            return item

    def isFull(self):
        return self.__size == self.__max_size

    def isEmpty(self):
        return self.__size == 0

    def showQueue(self):
        return " ".join(str(item) for item in self.__q[self.__front:self.__rear + 1])
