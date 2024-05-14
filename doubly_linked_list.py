class ListNode:
    def __init__(self, data):
        self.data = data
        self.prev = self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = self.tail = None

    def add_head(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = self.head = new_node

    def add_tail(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = self.tail = new_node

    def add_before(self, ref_node, data):
        if not self.head:
            raise ValueError("List is empty")

        new_node = ListNode(data)
        current = self.head
        found = False
        while current and not found:
            if current.data == ref_node:
                if current == self.head:
                    new_node.next = current
                    current.prev = new_node
                    self.head = new_node
                else:
                    new_node.prev = current.prev
                    new_node.next = current
                    current.prev.next = new_node
                    current.prev = new_node
                found = True
            current = current.next
        if not found:
            raise ValueError("Reference node not found")

    def add_after(self, ref_node, data):
        if not self.head:
            raise ValueError("List is empty")

        new_node = ListNode(data)
        current = self.head
        found = False
        while current and not found:
            if current.data == ref_node:
                if current == self.tail:
                    new_node.prev = current
                    current.next = new_node
                    self.tail = new_node
                else:
                    new_node.next = current.next
                    new_node.prev = current
                    current.next.prev = new_node
                    current.next = new_node
                found = True
            current = current.next
        if not found:
            raise ValueError("Reference node not found")

    def remove_head(self):
        if not self.head:
            raise ValueError("List is empty")

        data = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        return data

    def remove_tail(self):
        if not self.head:
            raise ValueError("List is empty")

        data = self.tail.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        return data

    def remove(self, data):
        if not self.head:
            raise ValueError("List is empty")

        current = self.head
        found = False
        while current and not found:
            if current.data == data:
                if current == self.head:
                    self.remove_head()
                elif current == self.tail:
                    self.remove_tail()
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                found = True
            current = current.next

    def traverse(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()
