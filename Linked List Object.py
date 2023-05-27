

""" doubly linked lists are collections of nodes that each contain a value and reference to the subsequent and previous node. The '__head' is the starting node for any iteration, whereas the '__tail' node's 'next_node' reference must point to 'None.' """
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

    """ add a new node to the end of the LL; if the list isn't empty (i.e., if '__tail' exists), update the 'next_node' reference of the current '__tail' to point to the new node. Also update the 'prev_node' reference of the new node to the current '__tail', then, set both to the new node. If the list is empty, set both to the new node; finally, increment '__size'. """
    def addNode(self, d):
        new_node = Node(d)
        if self.__tail:
            self.__tail.next_node = new_node
            new_node.prev_node = self.__tail
            self.__tail = new_node
        else:
            self.__head = new_node
            self.__tail = new_node
        self.__size += 1

    """ adds a new node at the specified index; if the index is > '__size', raise an exception. If the index == '__size', calls 'addNode' to add it to the end. If the index is 0, insert the new node at the beginning of the list by updating the 'next_node' reference of the new node to the current '__head', the 'prev_node' reference of the current 'head' to the new node, and setting '__head' to the new node. If the index isn't 0 nor == '__size', traverse the list to find the node at the specified index. Then, update the references of the new node and surrounding nodes to insert it correctly. If 'index = self.__size - 1', update '__tail' to the new node, before incrementing '__size.'' """
    def addNodeAt(self, d, index):
        if index > self.__size:
            raise IndexError("List index out of range.")
        if index == self.__size:
            self.addNode(d)
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

    """ deletes the first occurrence of a node, starting by traversing the list and searching for the it with the given data. Once found, update the references 'prev_node' and 'next_node' to remove the node from the list. If the node is the head, update '__head' to the next node; if it'sthe tail, update '__tail' to the previous node. Finally, decrement '__size.' """
    def deleteNode(self, d):
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

    """ traverses the list for a node and compare the data of each node w/ the given value; if these correspond, the index of the node is returned.  """
    def findNode(self, d):
        current_node = self.__head
        index = 0
        while current_node:
            if current_node.data == d:
                return f"Node {d} exists at index[{index}]."
            current_node = current_node.next_node
            index += 1
        raise ValueError("Node doesn't exist.")

    def showLL(self):
        l_list = []
        current_node = self.__head
        while current_node:
            l_list.append(current_node.data)
            current_node = current_node.next_node
        return l_list
