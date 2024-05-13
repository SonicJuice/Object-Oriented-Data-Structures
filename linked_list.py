class ListNode:
    def __init__(self, data):
        self.data = data
        self.prev = self.next = None

class LinkedList:
    def __init__(self):
        self.head = self.tail = None

    def append_left(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = self.head = new_node

    def append(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = self.tail = new_node

    def pop_left(self):
        if self.head:
            data = self.head.data
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None
            return data

    def pop(self):
        if self.head:
            data = self.tail.data
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None
            return data

    def traverse(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()
