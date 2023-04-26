
 
class CircularQueue(object):

    def __init__(self,qSize):
        self.__q = [None] * qSize
        self.__front = 0
        self.__rear = -1
        self.__size = 0
        self.__max_size = qSize

    def enQueue(self,item):
        if self.isFull():
            raise ValueError("Queue is full.")
        else:
            self.__rear = (self.__rear + 1) % self.__max_size
            self.__q[self.__rear] = item
            self.__size += 1
            return True

    def deQueue(self):
        if self.isEmpty():
            raise ValueError("Queue is empty.")
        else:
            self.__size -= 1
            item = self.__q[self.__front]
            self.__front = (self.__front + 1) % self.__max_size
            return item

    def isFull(self):
        return self.__size == self.__max_size
    
    def isEmpty(self):
        return self.__size == 0

    def __str__(self):
        return " ".join[(str(item) for item in self.__q[self.__front:self.__rear + 1])]
