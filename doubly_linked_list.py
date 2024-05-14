class ListNode:
    def __init__(self, data):
        self.data = data
        self.prev = self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = self.tail = None

    def appendleft(self, data):
        """ add a new node to the beginning of the list; if the list is empty, make it 
        the head and tail. """
        new_node = ListNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            """ set the new node's next to the current head. """
            new_node.next = self.head
            """ set the current head's previous to the new node. Finally, update the 
            head to point to the new node """
            self.head.prev = self.head = new_node

    def append(self, data):
        """ add a new node to the end of the list. """
        new_node = ListNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = self.tail = new_node

    def insert(self, data, pos):
        if pos <= 0:
            self.appendleft(data)
        elif pos >= self.index(self.tail.data):
            self.append(data)
        else:
            current = self.head
            index = 0
            while current and index < pos:
                current = current.next
                index += 1
            new_node = ListNode(data)
            new_node.prev, new_node.next = current.prev, current
            current.prev.next = current.prev = new_node

    def index(self, data):
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1

    def popleft(self):
        """ remove and return the node at the beginning of the list; if the list 
        isn't empty, save the current head. """
        if self.head:
            data = self.head.data
            """ if the head and tail are the same (there's only one node), set both to 
            None. """
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                """ update the head to be the node following the current head. Then, 
                set the prev pointer of the new head to None, as it's now the first 
                node. """
                self.head, self.head.prev = self.head.next, None
            return data

    def pop(self):
        """ remove and return the node at the end of the list. """
        if self.head:
            data = self.tail.data
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.tail, self.tail.next = self.tail.prev, None
            return data

    def remove(self, data):
        if self.head:
            current = self.head
            found = False
            while current and not found:
                if current.data == data:
                    if current == self.head:
                        self.popleft()
                    elif current == self.tail:
                        self.pop()
                    else:
                        current.prev.next, current.next.prev = current.next, current.prev
                    found = True
                current = current.next
