class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = self.prev = None

class DoublyLinkedList:
    def __init__(self, seq=()):
        self.head = self.tail = None
        self.size = 0
        self.extend(seq)

    def __iter__(self):
        node = self.head
        while node:
            yield node.value
            node = node.next

    def __len__(self):
        return self.size

    def __str__(self):
        return f"dll({list(self)})"

    def __repr__(self):
        return self.__str__()

    def __contains__(self, item):
        node = self.head
        while node:
            if node.value == item:
                return True
            node = node.next
        return False

    def __eq__(self, other):
        if type(other) is not type(self) or len(self) != len(other):
            return False
        node_self, node_other = self.head, other.head
        while node_self and node_other:
            if node_self.value != node_other.value:
                return False
            node_self, node_other = node_self.next, node_other.next
        return True

    def __getitem__(self, index):
        index = self.__validate_and_repair_index(index)
        if 0 <= index < self.size:
            if index <= self.size // 2:
                current = self.head
                for _ in range(index):
                    current = current.next
            else:
                current = self.tail
                for _ in range(self.size - 1, index, -1):
                    current = current.prev
            return current.value
        raise IndexError("List index out of range")

    def __setitem__(self, index, item):
        index = self.__validate_and_repair_index(index)
        if 0 <= index < self.size:
            if index <= self.size // 2:
                current = self.head
                for _ in range(index):
                    current = current.next
            else:
                current = self.tail
                for _ in range(self.size - 1, index, -1):
                    current = current.prev
            current.value = item
            return
        raise IndexError("List assignment index out of range")

    def __delitem__(self, index):
        index = self.__validate_and_repair_index(index)
        if 0 < index < self.size - 1:
            i = 0
            node = self.head
            while node:
                if i == index:
                    node.prev.next, node.next.prev = node.next, node.prev
                    self.size -= 1
                    return
                node = node.next
                i += 1
        elif index == 0 and self.head is not None:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            self.size -= 1
        elif index == self.size - 1 and self.head is not None:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
            self.size -= 1
        else:
            raise IndexError("List index out of range")

    def __validate_and_repair_index(self, index):
        if not isinstance(index, int):
            raise TypeError("List index must be an integer")
        index = self.size + index if index < 0 else index
        return index

    def append(self, item):
        new_node = ListNode(item)
        if not self.tail:
            self.tail = self.head = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = self.tail = new_node
        self.size += 1

    def appendleft(self, item):
        new_node = ListNode(item)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = self.head = new_node
        self.size += 1

    def insert(self, index, item):
        index = self.__validate_and_repair_index(index)
        if index == self.size:
            self.append(item)
        elif index == 0:
            self.appendleft(item)
        elif 0 < index < self.size:
            if index <= self.size // 2:
                current = self.head
                for _ in range(index):
                    current = current.next
            else:
                current = self.tail
                for _ in range(self.size - 1, index, -1):
                    current = current.prev
            new_node = ListNode(item)
            new_node.prev, new_node.next = current.prev, current
            current.prev.next = current.prev = new_node
            self.size += 1
        else:
            raise IndexError("List index out of range")

    def extend(self, seq):
        for i in seq:
            self.append(i)

    def extendleft(self, seq):
        for i in seq:
            self.appendleft(i)

    def index(self, item):
        node = self.head
        index = 0
        while node:
            if node.value == item:
                return index
            node = node.next
            index += 1
        return -1

    def count(self, item):
        count = 0
        node = self.head
        while node:
            if node.value == item:
                count += 1
            node = node.next
        return count
    
    def reverse(self):
        if self.size > 1:
            current = self.head
            while current:
                current.next, current.prev = current.prev, current.next
                current = current.prev
            self.head, self.tail = self.tail, self.head

    def pop(self):
        if self.size == 0:
            raise IndexError("List is empty")
        item = self.tail.value
        del self[self.size - 1]
        return item

    def popleft(self):
        if self.size == 0:
            raise IndexError("List is empty")
        item = self.head.value
        del self[0]
        return item

    def remove(self, item):
        if not self.head:
            raise IndexError("List is empty")
        else:
            if self.head.value == item:
                self.head = self.head.next
                if self.head:
                    self.head.prev = None
            elif self.tail.value == item:
                self.tail = self.tail.prev
                if self.tail:
                    self.tail.next = None
            else:
                node = self.head
                try:
                    while node:
                        if node.value == item:
                            node.prev.next = node.next
                            if node.next:
                                node.next.prev = node.prev
                            self.size -= 1
                            return
                        node = node.next
                except AttributeError:
                    raise ValueError("Value not in list") from None
            self.size -= 1

    def clear(self):
        self.head = self.tail = None
        self.size = 0
