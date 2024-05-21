from heapq import heappush, heappop

""" a queue derivation in which elements have an associated priority to compare with others. 
A sorted order is maintained to let new elements join where necessary while shuffling the existing 
ones accordingly. When two elements are of equal priority, they’ll follow their insertion order. """
class PriorityQueue(ThreadSafetyWrapper):
    def __init__(self, maxsize=None):
        """ items are typically in the form (priority, data). """
        self.queue = []
        super().__init__(maxsize)

    def enqueue(self, item, block=True):
        """ heapq.heappush/pop isn't thread safe. """
        with self.protect_put(block), self.mutex:
            """ heaps are binary trees for which every parent node has a value <= any of its 
            children (refered to as the heap invariant); heapq.heappush() pushes an item 
            onto the heap, maintaining the heap invariant. """
            heappush(self.queue, item)

    def dequeue(self, block=True):
        with self.protect_get(block), self.mutex:
            """ heapq.heappop() pops and returns the smallest item from the heap, maintaining 
            the heap invariant. """
            return heappop(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def qsize(self):
        return len(self.queue)
