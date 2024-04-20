""" doubly linked lists are collections of nodes that each contain a value and reference to the subsequent and previous node. 
The '__head' is the starting node for any iteration, whereas the '__tail' node's 'next_node' reference must point to 'None.' """


class Node(object):
    def __init__(self, d):
        self.next_node = None
        self.prev_node = None
        self.data = d


class LinkedList(object):
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__size = 0

    """ appends a new node to the end of the LL; if the list isn't empty (i.e., if __tail exists), update the next_node 
    reference of the current __tail to point to 'new_node'. Also update the prev_node reference of 'new_node' to the current 
    __tail, then, set both to the new node. If the list is empty, set both to the new node; finally, increment __size. """
    def append_node(self, d):
        new_node = Node(d)
        if self.__tail:
            self.__tail.next_node = new_node
            new_node.prev_node = self.__tail
            self.__tail = new_node
        else:
            self.__head = new_node
            self.__tail = new_node
        self.__size += 1

    """ inserts a node at the specified index; if it's > __size, raise an exception. If it's == __size, call addNode
    to add it to the end. If it's 0, insert new_node at the beginning of by updating the next_node reference of new_node
    to the current __head, the prev_node reference of the current head to the new_node, and setting  __head to new_node. 
    If it isn't 0 nor == __size, traverse the list to find the node at the specified index. Then, update the references of 
    new_node and surrounding nodes to insert it correctly. If index = self.__size - 1, update __tail to the new_node, before 
    incrementing __size. """
    def insert_Node(self, d, index):
        if index > self.__size:
            raise IndexError("List index out of range.")
        if index == self.__size:
            self.append_node(d)
            return True

        new_node = Node(d)
        if index == 0:
            new_node.next_node = self.__head
            self.__head.prev_node = new_node
            self.__head = new_node
            self.__size += 1
            return True
        else:
            current_node = self.__head
            i = 0
            while i < index:
                current_node = current_node.next_node
                i += 1

            new_node.next_node = current_node
            new_node.prev_node = current_node.prev_node
            current_node.prev_node.next_node = new_node
            current_node.prev_node = new_node

            if i == self.__size - 1:
                self.__tail = new_node

            self.__size += 1
            return True

        return False

    """ removes the first occurrence of a node, starting by traversing the list and searching for the it with the given data. Once 
    found, update the references 'prev_node' and 'next_node' to remove the node from the list. If the node is the head, update 
    '__head' to the next node; if it'sthe tail, update '__tail' to the previous node. Finally, decrement '__size.' """
    def remove_node(self, d):
        current_node = self.__head
        while current_node:
            if current_node.data == d:
                if current_node.prev_node:
                    current_node.prev_node.next_node = current_node.next_node
                else:
                    self.__head = current_node.next_node
                if current_node.next_node:
                    current_node.next_node.prev_node = current_node.prev_node
                else:
                    self.__tail = current_node.prev_node
                self.__size -= 1
                return True
            current_node = current_node.next_node
        raise ValueError("Node doesn't exist.")

    """ traverses the list for a node and compares the data of each node w/ the given value; if these correspond, the index of 
    the node is returned.  """
    def find_node(self, d):
        current_node = self.__head
        index = 0
        while current_node:
            if current_node.data == d:
                return f"Node {d} exists at index[{index}]."
            current_node = current_node.next_node
            index += 1
        raise ValueError("Node doesn't exist.")

    def show_linked_list(self):
        l_list = []
        current_node = self.__head
        while current_node:
            l_list.append(current_node.data)
            current_node = current_node.next_node
        return l_list
