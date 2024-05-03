import threading
from collections import deque


class Queue:
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        """ threading.semaphore() creates a synchronisation primitive (mechanism controlling 
        the access of multiple processes to shared resources in a concurrent system) that 
        manages a counter which is decremented/incremented by each acquire()/release() call. 
        The counter can never go below zero; when acquire() finds that it is zero, it blocks, 
        waiting until some other thread calls release(). """
        self._count = threading.Semaphore(0)
        self._init()

    def enqueue(self, item):
        if self.maxsize == 0 or self.qsize() < self.maxsize:
            self._enqueue(item)
            """ threading.semaphore.release(n=1) releases a semaphore, incrementing the 
            internal counter by n. When it was zero on entry and other threads are waiting for 
            it to become > zero again, wake up n threads. """
            self._count.release()
        else:
            raise ValueError("Queue is full.")

    def dequeue(self):
        """ threading.semaphore.acquire() acquirea a semaphore. If the internal counter > zero 
        on entry, decrement it by one and return True immediately. If the internal counter is 
        zero on entry, block until awoken by a call to release(). Once awoken (and the counter 
        > 0), decrement the counter by 1 and return True. Exactly one thread will be awoken by 
        each call to release(). """
        if not self._count.acquire():
            raise ValueError("Queue is empty.")
        return self._dequeue()

    def empty(self):
        """ returns True if the queue is empty. """
        return not self.queue

    def full(self):
        """ returns True if the queue has reached maxsize. """
        return self.maxsize != 0 and self.qsize() >= self.maxsize

    def qsize(self):
        """ return the current size of the queue. """
        return len(self.queue)

    def _init(self):
        self.queue = deque()

    def _enqueue(self, item):
        """ a deque (double-ended queue) is a container with thread-safe left and right-end 
        appending and popping methods. deque.append() adds an item to the right end of the 
        deque. """
        self.queue.append(item)

    def _dequeue(self):
        """ dequeue.popleft() removes and returns the left-most item. """
        return self.queue.popleft()
