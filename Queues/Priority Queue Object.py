

class PriorityQueue(object):
    def __init__(self, q_size):
        self.__q = []
        self.__size = 0
        self.__max_size = q_size

    """  a heap is a complete binary tree classified as either minheap (where each node is >= its children; the minimum element is always stored at the root, and each parent is < its children), or maxheap (where each node is <= its children; the maximum element is always stored at the root, and each parent is > its children). """
    def insert(self, item, priority):
        if self.isFull():
            raise ValueError("Queue is full.")
        else:
            self.__size += 1
            i = self.__size - 1
            self.__q.append((item, priority))
            """ inserts an item with a given priority, which is added to the end of the queue and moved up to its correct position based on its value. This involves comparing the item's PV with its parent and swapping positions until its correctly positioned. """
            while i > 0 and priority > self.__q[(i - 1) // 2][1]:
                self.__q[i], self.__q[(i - 1) // 2] = self.__q[(i - 1) // 2], self.__q[i]
                """ represents parent node's index. """
                i = (i - 1) // 2

    def delete(self):
        if self.isEmpty():
            raise ValueError("Queue is empty.")
        else:
            item, priority = self.__q[0]
            self.__q[0] = self.__q[-1]
            self.__q.pop()
            self.__size -= 1
            i = 0

            while i >= 0:
                """ represents child nodes' indexes. """
                left = 2 * i + 1
                right = 2 * i + 2
                largest = i
                if left < self.__size and self.__q[left][1] > self.__q[largest][1]:
                    largest = left
                if right < self.__size and self.__q[right][1] > self.__q[largest][1]:
                    largest = right
                if largest == i:
                    i = -1
                    """ remove the highest priority item from the queue and return it. The item is always first in the queue, which has the highest PV. After removing it, the remaining items are reorganized to maintain the PQ structure. This involves swapping the root with its largest child until the root is correctly positioned. """
                else:
                    self.__q[i], self.__q[largest] = self.__q[largest], self.__q[i]
                    i = largest
            return item, priority

    def alterPriority(self, item, new_priority):
        if self.isEmpty():
            raise ValueError("Queue is empty.")
        found = False
        i = 0
        """ searches for the item in the heap and replaces its current priority with the new one. Move the item up the PQ if the assigned value is <, and move it down if it's >. """
        while i < self.__size and not found:
            if self.__q[i][0] == item:
                found = True
            else:
                i += 1
        if not found:
            raise ValueError("Item doesn't exist.")
        old_priority = self.__q[i][1]
        self.__q[i] = (item, new_priority)
        if new_priority < old_priority:
            while i > 0 and new_priority > self.__q[(i - 1) // 2][1]:
                self.__q[i], self.__q[(i - 1) // 2] = self.__q[(i - 1) // 2], self.__q[i]
            i = (i - 1) // 2

    def isFull(self):
        return self.__size == self.__max_size

    def isEmpty(self):
        return self.__size == 0

    def showQueue(self):
        """ prints PQ contents in descending order by mapping to each item. """
        sorted_q = sorted(self.__q, key = lambda x: x[1], reverse = True)
        return " ".join(str(item) for item in sorted_q)
