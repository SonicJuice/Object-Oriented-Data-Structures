from tabulate import tabulate


class Node:
    def __init__(self, data):
        self.left = None
        self.data = data
        self.right = None

#------------------------------------------------------------------


""" trees are connected, undirected graph wo/ cycles; this means that it's impossible to find a path which 
returns to the start node without traversing an edge twice. Each node in a binary search tree can have up two children, 
storing data such that all nodes in the left subtree are < the root, and all nodes in the right subtree are >. """
class BinarySearchTree:
    def __init__(self, root_data):
        self.__branches = []
        root = Node(root_data)
        self.__branches.append(root)

    def addNode(self, data, current_node = 0):
        new_node = Node(data)
        """ iteratively moves down the tree based on the value of 'data'. If the data is < the current node's data, 
        it goes to the left child if it exists, or creates a new left child; if it's >= current node's data, it does the same 
        in the context of the right child. """
        while True:
            if self.__branches[current_node].data > data:
                if self.__branches[current_node].left is None:
                    self.__branches[current_node].left = len(self.__branches)
                    self.__branches.append(new_node)
                    return
                current_node = self.__branches[current_node].left
            else:
                if self.__branches[current_node].right is None:
                    self.__branches[current_node].right = len(self.__branches)
                    self.__branches.append(new_node)
                    return
                current_node = self.__branches[current_node].right

    def deleteNode(self, data, current_node = 0, parent_node = None):
        while current_node is not None and self.__branches[current_node].data != data:
            parent_node = current_node
            if self.__branches[current_node].data > data:
                current_node = self.__branches[current_node].left
            else:
                current_node = self.__branches[current_node].right

        if current_node is None:
            raise ValueError("Node doesn't exist.")

        """ if 'node' is a leaf, remove it from the list. """
        if self.__branches[current_node].left is None and self.__branches[current_node].right is None:
            if parent_node is None:
                self.__branches = []
            elif self.__branches[parent_node].left == current_node:
                self.__branches[parent_node].left = None
            else:
                self.__branches[parent_node].right = None

            """ if it has one child, the child is promoted to take the place of the deleted node. """
        elif self.__branches[current_node].left is None or self.__branches[current_node].right is None:
            child_index = self.__branches[current_node].left if self.__branches[current_node].left is not None else self.__branches[current_node].right
            if parent_node is None:
                self.__branches = self.__branches[child_index:]
            elif self.__branches[parent_node].left == current_node:
                self.__branches[parent_node].left = child_index
            else:
                self.__branches[parent_node].right = child_index

                """ if it has two children, it finds the node's successor (i.e., the smallest node in the right subtree),
                replaces the node's data w/ the successor's data, and then removes the successor. """
        else:
            successor_parent = current_node
            successor = self.__branches[current_node].right
            while self.__branches[successor].left is not None:
                successor_parent = successor
                successor = self.__branches[successor].left
            self.__branches[current_node].data = self.__branches[successor].data

            if self.__branches[successor_parent].left == successor:
                self.__branches[successor_parent].left = self.__branches[successor].right
            else:
                self.__branches[successor_parent].right = self.__branches[successor].right
              
    def showSubTree(self, data, current_node = 0):
        while current_node is not None and self.__branches[current_node].data != data:
            if self.__branches[current_node].data > data:
                current_node = self.__branches[current_node].left
            else:
                current_node = self.__branches[current_node].right

        if current_node is None:
            raise ValueError("Node doesn't exist.")

        """ describes the subtree rooted at the node w/ the specified value, first traversing the tree to find the node with the specified value. Once it finds the node, determine the type of node based on whether it's a leaf, has one child, or has two children, and returns a string describing the node. """
        if current_node == 0:
            left_child_index = self.__branches[current_node].left
            left_child_data = self.__branches[left_child_index].data if left_child_index is not None else None
            right_child_index = self.__branches[current_node].right
            right_child_data = self.__branches[right_child_index].data if right_child_index is not None else None

            if left_child_index is None and right_child_index is None:
                return f"({data}) is the root of the tree with no children."
            elif left_child_index is None:
                return f"({data}) is the root of the tree with one child: right child ({right_child_data})."
            elif right_child_index is None:
                return f"({data}) is the root of the tree with one child: left child ({left_child_data})."
            else:
                return f"({data}) is the root of the tree with two children: left child ({left_child_data}), right child ({right_child_data})."

        if self.__branches[current_node].left is None and self.__branches[current_node].right is None:
            return f"({data}) is a leaf node."

        if self.__branches[current_node].left is None or self.__branches[current_node].right is None:
            child_index = self.__branches[current_node].left if self.__branches[current_node].left is not None else self.__branches[current_node].right
            child_data = self.__branches[child_index].data
            return f"({data}) has one child: ({child_data})."

        left_child_index = self.__branches[current_node].left
        left_child_data = self.__branches[left_child_index].data
        right_child_index = self.__branches[current_node].right
        right_child_data = self.__branches[right_child_index].data
        return f"({data}) has two children: left child ({left_child_data}), right child ({right_child_data})."

    """ visit left sub-tree, root, right sub-tree (starting to the left of the root, output the 
    corresponding data when passing beneath a node). """
    def inOrderTraversal(self, current_node = 0):
        if current_node is None:
            return []
        traversal = []
        traversal += self.inOrderTraversal(self.__branches[current_node].left)
        traversal.append(self.__branches[current_node].data)
        traversal += self.inOrderTraversal(self.__branches[current_node].right)
        return traversal

    """ visit the root, left sub-tree, right sub-tree (starting to the left of the root, output the corresponding data 
    when passing to the left of a node). """
    def preOrderTraversal(self, current_node = 0):
        if current_node is None:
            return []
        traversal = []
        traversal.append(self.__branches[current_node].data)
        traversal += self.preOrderTraversal(self.__branches[current_node].left)
        traversal += self.preOrderTraversal(self.__branches[current_node].right)
        return traversal

    """ visit left sub-tree, right sub-tree, root (starting to the right of the root, output the corresponding data
    when passing to the right a node). """
    def postOrderTraversal(self, current_node = 0):
        if current_node is None:
            return []
        traversal = []
        traversal += self.postOrderTraversal(self.__branches[current_node].left)
        traversal += self.postOrderTraversal(self.__branches[current_node].right)
        traversal.append(self.__branches[current_node].data)
        return traversal

    """ BSTs are said to balanced if the heights of the left and right subtrees of any node differ by at most one. """
    def balanceBST(self):
        sorted_nodes = self.inOrderTraversal()

        def __constructBalancedBST(start, end):
            if start > end:
                return
            """ calculate the middle index between the start and end indices '(start + end) // 2', being the index of the node 
            that will become the root of the subtree. create a new 'Node' with the value of the node at the middle index. """
            mid = (start + end) // 2
            node = Node(sorted_nodes[mid])
            """ recursively call __constructBalancedBST for the left half of the range, from start to mid - 1, and assign 
            the returned node to the left and 'right' attributes of the current node. """
            node.left = __constructBalancedBST(start, mid - 1)
            node.right = __constructBalancedBST(mid + 1, end)
            return node
        """ call the '__constructBalancedBST' function w/ parameters to construct a balanced BST
        w/ the sorted nodes. """
        new_root = __constructBalancedBST(0, len(sorted_nodes) - 1)
        self.__branches = []
        
        def __depthFirst(node):
            if node is not None:
                """ DF that adds each node to '__branches' and returns a new node index; this is used to track nodes 
                after rebalancing. Subtrees of the node are then recursively traversed. """
                new_node_index = len(self.__branches)
                self.__branches.append(node)
                node.left = __depthFirst(node.left)
                node.right = __depthFirst(node.right)
                return new_node_index
        __depthFirst(new_root)
  
    """ 'tree[i]' indicates the index of the child represented by the relevant pointers; None indicates that there's no child 
    on the relevant side. """
    def showBST(self):
        table = []
        for i in range(len(self.__branches)):
            node = self.__branches[i]
            table.append([f"tree[{i}]", node.left, node.data, node.right])
        headers = ["Left", "Data", "Right"]
        return tabulate(table, headers)
