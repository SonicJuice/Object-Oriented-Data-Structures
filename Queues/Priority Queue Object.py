

class PriorityQueue(object):
    def __init__(self, q_size):
        self.__q = [None] * q_size
        self.__size = 0
        self.__max_size = q_size

    """ a heap is a complete binary tree that satisfies the heap property. They can be minheap (where each node is >= its children; the minimum element is always stored at the root, and each parent is < its children), or maxheap (where each node is <= its children; the maximum element is always stored at the root, and each parent is > its children). """
    def enQueue(self, item, priority):
        if self.isFull():
            raise ValueError("Queue is full.")
        else:
            self.__size += 1
            i = self.__size - 1
            self.__q[i] = (item, priority)
            while i > 0 and priority > self.__q[(i - 1) // 2][1]:
                self.__q[i], self.__q[(i - 1) // 2] = self.__q[(i - 1) // 2], self.__q[i]
                i = (i - 1) // 2
            return True

    def deQueue(self):
        if self.isEmpty():
            raise ValueError("Queue is empty.")
        else:
            item, priority = self.__q[0]
            self.__q[0] = self.__q[self.__size - 1]
            self.__q[self.__size - 1] = None
            self.__size -= 1
            i = 0

            while i >= 0:
                left = 2 * i + 1
                right = 2 * i + 2
                largest = i
                if left < self.__size and self.__q[left][1] > self.__q[largest][1]:
                    largest = left
                if right < self.__size and self.__q[right][1] > self.__q[largest][1]:
                    largest = right
                if largest == i:
                    i = -1
                else:
                    self.__q[i], self.__q[largest] = self.__q[largest], self.__q[i]
                    i = largest
            return item, priority

    def isFull(self):
        return self.__size == self.__max_size

    def isEmpty(self):
        return self.__size == 0

    def showQueue(self):
        return " ".join(str(item) for item in self.__q[:self.__size])

queue = PriorityQueue(5)

queue.enQueue('apple', 2)
queue.enQueue('banana', 3)
queue.enQueue('orange', 1)

print(queue.showQueue())  # Output: ('banana', 3) ('apple', 2) ('orange', 1) None None

item, priority = queue.deQueue()
print(f"Removed item: {item} with priority: {priority}")  # Output: Removed item: banana with priority: 3

print(queue.showQueue())

queue.enQueue('kiwi', 4)
queue.enQueue('grape', 5)

print(queue.showQueue())

queue.enQueue('watermelon', 6)
