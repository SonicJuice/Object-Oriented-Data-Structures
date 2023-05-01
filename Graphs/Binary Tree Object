

class Node(object):
    def __init__(self, data, left=-1, right=-1):
        self.__left = left
        self.__data = data
        self.__right= right

    def setLeft(self, left_value):
        self.__left = left_value

    def setRight(self, right_value):
        self.__right = right_value

    def setData(self, data_value):
        self.__data = data_value

    def getLeft(self):
        return self.__left

    def getRight(self):
        return self.__right

    def getData(self):
        return self.__data

    def __str__(self):
       output = "{}\t{}\t{}".format(self.getLeft(),self.getData(),self.getRight())
       return output
    
#---------------------------------------------------------------------------


class BinaryTree(object):
    def __init__(self, root_data):
        self.__branches  = []
        root = Node(root_data)
        self.__branches.append(root)

    def addNode(self, data):
        current_node = 0
        found_end = False
        to_left = True
        while not found_end:
            if self.__branches[current_node].getData() >= data:
                if self.__branches[current_node].getLeft() == -1:
                    found_end = True
                else:
                    current_node = self.__branches[current_node].getLeft()
            else:
                if self.__branches[current_node].getRight() == -1:
                    found_end = True
                    to_left = False
                else:
                    current_node = self.__branches[current_node].getRight()
        next_index = len(self.__branches)
        self.__branches.append(Node(data))
        if to_eft:
            self.__branches[current_node].setLeft(next_index)
        else:
            self.__branches[current_node].setRight(next_index)

    def inOrder(self, current_node=0, visited=[]):
        if self.__branches[current_node].getLeft() != -1:
            self.inOrder(self.__branches[current_node].getLeft(), visited)
        visited.append(current_node)
        if self.__branches[current_node].getRight() != -1:
            self.inOrder(self.__branches[current_node].getRight(), visited)
        return [self.__branches[i].getData() for i in visited]
        
    def preOrder(self, current_node, visited=[]):
        visited.append(current_node)
        if self.__branches[current_node].getLeft() != -1:
            self.preOrder(self.__branches[current_node].getLeft(), visited)
        if self.__branches[current_node].getRight() != -1:
            self.preOrder(self.__branches[current_node].getRight(), visited)
        return [self.__branches[i].getData() for i in visited]

    def postOrder(self, currentNode, visited=[]):
        if self.__branches[current_node].getLeft() != -1:
            self.postOrder(self.__branches[current_node].getLeft(), visited)
        if self.__branches[current_node].getRight() != -1:
            self.postOrder(self.__branches[current_node].getRight(), visited)
        visited.append(current_node)
        return [self.__branches[index].getData() for index in visited]

    def __str__(self):
        output = "i\tData\tLeft\tRight\n"
        for i in range(len(self.__branches)):
            output += str(i) + "\t" + str(self.__branches[i]) + "\n"
        return output

    def isBalanced(self):
        pass
