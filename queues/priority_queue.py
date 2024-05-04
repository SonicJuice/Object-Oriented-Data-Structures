from queue import Queue
from heapq import heappush, heappop


class PriorityQueue(Queue):
    def _init(self):
        """ items are typically in the form (priority, data). """
        self.queue = []

    def _enqueue(self, item):
        """ heaps are binary trees for which every parent node has a value <= any of its 
        children (refered to as the heap invariant); heapq.heappush() pushes an item 
        onto the heap, maintaining the heap invariant. """
        heappush(self.queue, item)

    def _dequeue(self):
        """ heapq.heappop() pops and returns the smallest item from the heap, maintaining 
        the heap invariant. """
        return heappop(self.queue)
