class ListNode:
    def __init__(self, data):
        self.data = data
        self.prev = self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        if index < 0:
            index += len(self)
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def append(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def appendleft(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = self.head = new_node
        self.size += 1

    def insert(self, index, data):
        if index < 0:
            index += len(self)
        if index == 0:
            self.appendleft(data)
        elif index == len(self):
            self.append(data)
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            new_node = ListNode(data)
            new_node.prev, new_node.next = current.prev, current
            if current.prev:
                current.prev.next = new_node
            current.prev = new_node
            self.size += 1

    def pop(self):
        if not self.tail:
            raise IndexError("pop from empty list")
        data = self.tail.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
        return data

    def popleft(self):
        if not self.head:
            raise IndexError("pop from empty list")
        data = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return data

    def remove(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self.size -= 1
                return
            current = current.next
