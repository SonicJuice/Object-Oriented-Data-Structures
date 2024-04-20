

class Stack(object):
    def __init__(self, max_size, iterable=False):
        self.stack = []
        self.size = 0
        self.max_size = max_size
        """ constructor method may take iterable, which specifies whether the stack should be initialised with items 
        from an iterable. __stack is then intialised to represent the stack, as are the initial size __size, and the maximum 
        size, self.max_size. """
        if iterable:
            for item in iterable:
                self.push(item)

    def push(self,item):
        """ adds a new item to the top of stack; returns False if stack is full. """
        if self.isFull() == False:
            """ .insert places a specified element at a specified list index. """
            self.stack.insert(0, item)
            self.size += 1
            return True
        else:
            return False

    def pop(self):
        """ returns top item from the stack. """
        if self.isEmpty() == False:
            self.size -= 1
            """ .pop() removes an item from a list according to its index value.  """
            return self.stack.pop(0)
        else:
            raise ValueError("Stack is empty.")

    def peek(self):
        """ returns the top item without removing it. """
        if self.is_empty() == False:
            self.size -= 1
            return self.stack[0]
        else:
            raise ValueError("Stack is empty.")

    def size(self):
        """ returns no. of items in stack. """
        return self.size

    def is_full(self):
        return self.size == self.max_size

    def is_empty(self):
        return self.size == 0
  
    def show_stack(self):
        output = ""
        for item in self.stack:
            output += str(item) + "\n"
        return output
