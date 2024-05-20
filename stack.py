class Stack(ThreadSafetyWrapper):
    def __init__(self, maxsize=None):
        self.stack = deque()
        super().__init__(maxsize)

    def push(self, item, block=True):
        with self.protect_put(block):
            self.stack.append(item)

    def pop(self, block=True):
        with self.protect_get(block):
            """ dequeue.pop() removes and returns the left-most item. """
            return self.stack.pop()
            
    def empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)
