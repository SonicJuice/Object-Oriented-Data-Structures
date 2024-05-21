from collections import deque

""" processes elements on a first-come, first-served basis. A new element is only allowed 
to join the queue via the tail, while the oldest must leave from the head. This causes 
all of its followers to shift one position towards the head. """
class Queue(ThreadSafetyWrapper):
    def __init__(self, maxsize=None):
        """ deques (double-ended queues) are thread-safe containers supporting thread-safe 
        left- and right-end appending and popping. """
        self.queue = deque()
        """ super().__init__(maxsize) ensures that the initialisation logic defined in 
        the superclass ThreadSafetyWrapper is executed when creating instances of Queue. """
        super().__init__(maxsize)

    def enqueue(self, item, block=True):
        """ with first calls the __enter__() method of the context manager to acquiring any necessary 
        resources. Once the context has been established, the associated block of code is executed. 
        After the block has been executed, (either successfully or due to an exception), 
        it calls __exit__() to release any acquired resources and perform cleanup operations. """
        with self.protect_put(block):
            """ deque.append() adds an item to the right end of the deque. """
            self.queue.append(item)

    def dequeue(self, block=True):
        with self.protect_get(block):
            """ dequeue.popleft() removes and returns the left-most item. """
            return self.queue.popleft()

    def empty(self):
        return len(self.queue) == 0

    def qsize(self):
        return len(self.queue)
