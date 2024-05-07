import threading
from collections import deque


class Empty(Exception):
    """ Raised by Queue.dequeue(block=0). """
    pass

class Full(Exception):
    """ Raised by Queue.enqueue(block=0). """
    pass

class ShutDown(Exception):
    """ Raised when enqueue/dequeue with shut-down queue. """


class Queue:
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self._init()

        """ the threading.Lock() class helps prevent race conditions by giving only one thread 
        access to the critical section of code or shared resource. Other threads attempting to 
        acquire the lock are blocked until it's released by the owning thread. """
        self.mutex = threading.Lock()
        """ notify not_empty whenever an item is added to the queue; a thread waiting to 
        dequeue is notified then. the threading.Condition() class implements a condition variable 
        objects. This allows one or more threads to wait until they are notified by another. """
        self.not_empty = threading.Condition(self.mutex)
        """ notify not_full whenever an item is removed from the queue; a thread waiting to 
        enqueue is notified then. """
        self.not_full = threading.Condition(self.mutex)
        """ notify all_tasks_done whenever the number of unfinished tasks drops to zero; 
        thread waiting to join() is notified to resume. """
        self.all_tasks_done = threading.Condition(self.mutex)

        self.unfinished_tasks = 0
        self.is_shutdown = False

    def task_done(self):
        """ Indicate that a formerly enqueued task is complete. For each dequeue() 
        used to fetch a task, a subsequent call to this tells the queue that task has finished 
        being processed. """
        with self.all_tasks_done:
            unfinished = self.unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    """ raised when task_done() is called more times than there are enqueued tasks. """
                    raise ValueError("task_done() called too many times")
                """ threading.Condition.notify_all() wakes up all threads waiting on the condition. """
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished

    def join(self):
        """ Block until all items have been gotten and processed. unfinished_tasks 
        increments/decrements whenever an item is added to the queue/a consumer thread 
        calls task_done(). When the count of unfinished tasks drops to zero, join() 
        unblocks. """
        with self.all_tasks_done:
            """ while there are unfinished tasks, wait for all_tasks_done to be notified. """
            while self.unfinished_tasks:
                """ threading.Condition.wait() waits until notified or until a timeout occurs. If the 
                calling thread has not acquired the lock when this method is called, a RuntimeError is 
                raised. This method releases the underlying lock, and then blocks until it's awakened 
                by a notify() or notify_all() call for the same condition variable in another thread. 
                Once awakened it re-acquires the lock and returns. """
                self.all_tasks_done.wait()

    def qsize(self):
        with self.mutex:
            return self._qsize()

    def empty(self):
        with self.mutex:
            return not self._qsize()

    def full(self):
        with self.mutex:
            return 0 < self.maxsize <= self._qsize()

    def enqueue(self, item, block=True):
        """ put an item onto the queue. If block is True, block if necessary until a free slot is 
        available. Otherwise, put an item on the queue if a free slot is immediately available, 
        else raise Full. Raise ShutDown if the queue has been shut down. """
        with self.not_full:
            if self.is_shutdown:
                raise ShutDown
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                else:
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()
                        if self.is_shutdown:
                            raise ShutDown
            self._enqueue(item)
            self.unfinished_tasks += 1
            """ threading.Condition.notify(n=1) wakes up at most n of the threads waiting for the 
            condition variable; it's a no-op if no threads are waiting. """
            self.not_empty.notify()

    def dequeue(self, block=True):
        """ Remove and return an item from the queue. If block is True, block if necessary until an 
        item is available. Otherwise, return an item if one is immediately available, else 
        raise Empty. Raise ShutDown if the queue has been shut down and is empty, or if 
        the queue has been shut down immediately. """
        with self.not_empty:
            if self.is_shutdown and not self._qsize():
                raise ShutDown
            if not block:
                if not self._qsize():
                    raise Empty
            else:
                while not self._qsize():
                    self.not_empty.wait()
                    if self.is_shutdown and not self._qsize():
                        raise ShutDown
            item = self._dequeue()
            self.not_full.notify()
            return item

    def shutdown(self, immediate=False):
        """ Shut-down the queue, making enqueues and dequeues raise ShutDown. 
        By default, dequeues will only raise once the queue is empty. immediate=True
        makes dequeues raise immediately instead. All blocked callers of enqueue() and 
        dequeue() will be unblocked. If immediate, a task is marked as done for each item 
        remaining in the queue, which may unblock callers of join(). """
        with self.mutex:
            self.is_shutdown = True
            if immediate:
                while self._qsize():
                    self._dequeue()
                    if self.unfinished_tasks > 0:
                        self.unfinished_tasks -= 1
                self.all_tasks_done.notify_all()
            self.not_empty.notify_all()
            self.not_full.notify_all()

    def _init(self):
        """ deques (double-ended queues) are thread-safe containers supporting thread-safe 
        left- and right-end appending and popping. """
        self.queue = deque()

    def _qsize(self):
        return len(self.queue)

    def _enqueue(self, item):
        """ deque.append() adds an item to the right end of the deque. """
        self.queue.append(item)

    def _dequeue(self):
        """ dequeue.popleft() removes and returns the left-most item. """
        return self.queue.popleft()
