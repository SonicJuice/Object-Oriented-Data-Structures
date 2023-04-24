

class PriorityQueue(object):
    def __init__(self, q_size):
        self.__q = [None] * q_size
        self.__size = 0
        self.__max_size = q_size

    """ for reference, a heap is a complete binary tree which satisfies either of the following order properties: 'the value of each node is >= its
    parent's, with the minimum-value element at the root' (min-heap), or 'the value of each node is <= its parent's, with the maximum-value element
    at the root' (max-heap). """
    def enQueue(self, item, priority):
        if self.isFull():
            return False
        else:
            self.__size += 1
            i = self.__size - 1
            """ item w/ its coresponding priority is queued; if the queue isn't full, increment attribute '.__size' by one. Then, add the pair
            as a tuple to the end of the list, before 'sifting up' to maintain the heap property of the PQ,
            where the item w/ the highest priority is moved up the heap until it reaches its correct position. """
            self.__q[i] = (item, priority)
            while i > 0 and priority > self.__q[(i - 1) // 2][1]:
                """ achieved via a while loop that compares the priority of the item with its parent (calculated via '//` 2'),
                and swaps them if the priority of the item is greater. """
                self.__q[i], self.__q[(i - 1) // 2] = self.__q[(i - 1) // 2], self.__q[i]
                i = (i - 1) // 2
            return True

    def deQueue(self):
        """ if the PQ isn't empty, retrieve the item and its priority from the first element of the list '__q' which represents the root of the heap.
        It then replaces the root with the last item in'__q', and sets the last item to None. """
        if self.isEmpty():
            return None
        else:
            item, priority = self.__q[0]
            self.__q[0] = self.__q[self.__size - 1]
            self.__q[self.__size - 1] = None
            self.__size -= 1
            i = 0
            """ next, a 'sift down' operation is performed to maintain the heap property of the PQ, where the root
           is moved down the heap until it reaches its correct position. This is achieved via a while loop that compares the priority of the root
           with its children (calculated using 2 * i + 1 and 2 * i + 2, where i is the index of the root),and swaps them if the priority of
           the root item is lower. Finally, it returns the removed item and its priority as a tuple. """
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

    def __str__(self):
        return " ".join(str(item) for item in self.__q[:self.__size])
