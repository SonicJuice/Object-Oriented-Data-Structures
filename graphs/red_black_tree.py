import enum
from dataclasses import dataclass
from typing import Any, Union, Optional, Iterator
from threading import Lock

""" sublassing enum.Enum creates an enumeration (set of symbolic names bound to unique 
constants. Within an enumeration, values can be compared by identity, and the enumeration 
itself can be iterated over). """
class Color(enum.Enum):
    """ enum.auto() assigns automatic values (consecutive integers by default) to enum 
    members. """
    RED = enum.auto()
    BLACK = enum.auto()

""" dataclasses.@dataclass automatically generates special methods (__init__(), __repr__(), 
__eq__()) based on class attributes (__hash__() if all attributes are immutable). frozen=True 
allows for immutable instantiations. """
@dataclass(frozen=True)
class Leaf:
    color = Color.BLACK

@dataclass
class Node:
    """ typing.Any/Union tells the type checker that a variable can be of any/one 
    of several type(s). The former allows it to accept any value without TypeErrors. """
    key: Any
    data: Any
    left: Union["Node", Leaf] = Leaf()
    right: Union["Node", Leaf] = Leaf()
    parent: Union["Node", Leaf] = Leaf()
    color: Color = Color.RED

""" Red-Black-Tree-Property (RBTP):
1). The root is black.
2). Every leaf is black.
3). If a node is red, both of its children are black.
4). Every path from a node to any of its leaves contains the same number of blacks. """
class RBTree:
    def __init__(self):
        """ all the leaves are NIL and the root's parent can point to NIL, so make this,
        and all other nodes supported to point to NIL, point to a single NIL node. 
        The use of only one NIL node instance saves space. """
        self._NIL: Leaf = Leaf()
        self.root: Union[Node, Leaf] = self._NIL
        self._mutex = Lock()

    def empty(self) -> bool:
        return self.root is None or self.root == self._NIL

    """ typing.Optional denotes that a variable can be of a specified type or None. """
    def search(self, key: Any) -> Optional[Node]:
        with self._mutex:
            return self._search(key=key)

    def _search(self, key: Any) -> Optional[Node]:
        """ look for a node with the given key. """
        current = self.root

        """ iterate from the root and compare the key with each node's from along the 
        path. """
        while isinstance(current, Node):
            """ if a key matches, the node has been found. """
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current
        """ if the Leaf is reached, the node doesn't exist. """
        raise NodeNotFoundError

    def insert(self, key: Any, data: Any) -> None:
        with self._mutex:
            new_node = Node(key=key, data=data, color=Color.RED)
            parent: Union[Node, Leaf] = self._NIL
            current: Union[Node, Leaf] = self.root

            """ iterate from the root to find the correct position for the new, red node. """
            while isinstance(current, Node):
                parent = current
                if new_node.key < current.key:
                    current = current.left
                elif new_node.key > current.key:
                    current = current.right
                else:
                    raise DuplicateKeyError
            new_node.parent = parent
            """ if the parent is a leaf, make the new node into the black root. """
            if isinstance(parent, Leaf):
                new_node.color = Color.BLACK
                self.root = new_node
            else:
                """ otherwise, attach the new node as the appropriate child of the parent. """
                if new_node.key < parent.key:
                    parent.left = new_node
                else:
                    parent.right = new_node
                self._insert_fixup(new_node)

    def delete(self, key: Any) -> None:
        """ find the node to be deleted and maintain its colour. """
        with self._mutex:
            if (deleting_node := self._search(key=key)) and isinstance(deleting_node, Node):
                original_color = deleting_node.color

                """ if deleting_node has no children/only one left or right child. """
                if isinstance(deleting_node.left, Leaf):
                    replacing_node = deleting_node.right
                    """ replace deleting_node with NIL or the only child. """
                    self._transplant(deleting_node=deleting_node, replacing_node=replacing_node)
                    if original_color == Color.BLACK and isinstance(replacing_node, Node):
                        self._delete_fixup(fixing_node=replacing_node)

                elif isinstance(deleting_node.right, Leaf):
                    replacing_node = deleting_node.left
                    self._transplant(deleting_node=deleting_node, replacing_node=replacing_node)
                    if original_color == Color.BLACK and isinstance(replacing_node, Node):
                        self._delete_fixup(fixing_node=replacing_node)

                else:
                    """ if deleting_node has two children, find its successor replacing_node 
                    and keep its color. """
                    replacing_node = self.leftmost(deleting_node.right)
                    original_color = replacing_node.color
                    replacing_replacement = replacing_node.right

                    if replacing_node.parent == deleting_node:
                        if isinstance(replacing_replacement, Node):
                            replacing_replacement.parent = replacing_node
                    else:
                        """ remove replacing_node and keep tracing the node to replace 
                        replacing_node (either NIL or its original right child). """
                        self._transplant(replacing_node, replacing_node.right)
                        replacing_node.right = deleting_node.right
                        replacing_node.right.parent = replacing_node

                    """ replace deleting_node with replacing_node, giving it the former's 
                    colour. """
                    self._transplant(deleting_node, replacing_node)
                    replacing_node.left = deleting_node.left
                    replacing_node.left.parent = replacing_node
                    replacing_node.color = deleting_node.color

                    if original_color == Color.BLACK and isinstance(replacing_replacement, Node):
                        self._delete_fixup(fixing_node=replacing_replacement)

    """ @staticmethods don't require access to the instance or class they belong to. This 
    means they can be called on a class or instance without any reference to them. """
    @staticmethod
    def height(node: Union[Leaf, Node]) -> int:
        """ represents the longest length down to a leaf from the root. """
        if isinstance(node, Node):
            """ recursively increment the height by one for each child's height. If a node 
            has two children, obtain the bigger height and increase the highest by one. """
            if isinstance(node.left, Node) and isinstance(node.right, Node):
                return (max(RBTree.height(node.left), RBTree.height(node.right)) + 1)

            if isinstance(node.left, Node):
                return RBTree.height(node=node.left) + 1

            if isinstance(node.right, Node):
                return RBTree.height(node=node.right) + 1
        return 0

    @staticmethod
    def leftmost(node: Node) -> Node:
        """ left/rightmost node contains the minimum/maximum key in a given subtree. 
        Since these can be retrieved from any given subtree (if not the entire tree), 
        the parameter is the root of the given subtree. """
        current_node = node
        while isinstance(current_node.left, Node):
            current_node = current_node.left
        return current_node

    @staticmethod
    def rightmost(node: Node) -> Node:
        current_node = node
        while isinstance(current_node.right, Node):
            current_node = current_node.right
        return current_node

    @staticmethod
    def successor(node: Node) -> Union[Node, Leaf]:
        """ if the right child of the given node isn't empty, the leftmost node of the 
        left subtree is the predecessor. """
        if isinstance(node.right, Node):
            return RBTree.leftmost(node=node.right)

        """ if the right child of the given node is empty, move upwards until a node that 
        is the left child of its parent is encountered. """
        parent = node.parent
        while isinstance(parent, Node) and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    @staticmethod
    def predecessor(node: Node) -> Union[Node, Leaf]:
        if isinstance(node.left, Node):
            return RBTree.rightmost(node=node.left)

        parent = node.parent
        while isinstance(parent, Node) and node == parent.left:
            node = parent
            parent = parent.parent
        return node.parent

    """ typing.iterator[tuple[Any, Any]] denotes that a variable implements __iter__() 
    and __next__() to yield tuples containing two elements of any type. """
    def inorder_traverse(self) -> Iterator[tuple[Any, Any]]:
        return self._inorder_traverse(node=self.root)

    def preorder_traverse(self) -> Iterator[tuple[Any, Any]]:
        return self._preorder_traverse(node=self.root)

    def postorder_traverse(self) -> Iterator[tuple[Any, Any]]:
        return self._postorder_traverse(node=self.root)

    def _left_rotate(self, node_x: Node) -> None:
        node_y = node_x.right
        if isinstance(node_y, Leaf):
            raise RuntimeError("Invalid left rotate")

        """ turn node_y's subtree into node_x's. """
        node_x.right = node_y.left
        if isinstance(node_y.left, Node):
            node_y.left.parent = node_x
        node_y.parent = node_x.parent

        """ if node x's parent is a Leaf. """
        if isinstance(node_x.parent, Leaf):
            """ make node_y into the new root. """
            self.root = node_y
        elif node_x == node_x.parent.left:
            """ otherwise, update node_x's parent. """
            node_x.parent.left = node_y
        else:
            node_x.parent.right = node_y

        """ node_x's right child can't be a Leaf (NIL), as this would be redundant to 
        rotate. """
        node_y.left = node_x
        node_x.parent = node_y

    def _right_rotate(self, node_x: Node) -> None:
        node_y = node_x.left
        if isinstance(node_y, Leaf):
            raise RuntimeError("Invalid right rotate")

        node_x.left = node_y.right
        if isinstance(node_y.right, Node):
            node_y.right.parent = node_x
        node_y.parent = node_x.parent

        if isinstance(node_x.parent, Leaf):
            self.root = node_y
        elif node_x == node_x.parent.right:
            node_x.parent.right = node_y
        else:
            node_x.parent.left = node_y

        node_y.right = node_x
        node_x.parent = node_y

    def _insert_fixup(self, fixing_node: Node) -> None:
        """ RBTP 4 holds after insertion, as the new red node replaces a Leaf (NIL), 
        but its children are also Leaves. However, if its parent is also red, RBTP 3
        would be violated. RBTP 1 could also be violated if a new node is the root, or 
        the root becomes red, whilst fixing RBTP 3. Fixing RBTP 3 can be thought of in 
        six cases. """
        while fixing_node.parent.color == Color.RED:
            if fixing_node.parent == fixing_node.parent.parent.left: 
                parent_sibling = fixing_node.parent.parent.right 

                """ Case 1). if the new node's parent's location is the left child, the 
                parent's sibling is red, and the new node's location doesn't matter. """
                if parent_sibling.color == Color.RED:
                    """ make fixing_node's parent and the parent's sibling black. """
                    fixing_node.parent.color = Color.BLACK
                    parent_sibling.color = Color.BLACK
                    """ make the fixing node's grandparent red. """
                    fixing_node.parent.parent.color = Color.RED 
                    """ move to the current location of the grandparent. """
                    fixing_node = fixing_node.parent.parent

                else:
                    """ Case 2). if the new node's parent's location is the left child, 
                    the parent's sibling is black, and the new node's location is the 
                    right child. """
                    if fixing_node == fixing_node.parent.right: 
                        fixing_node = fixing_node.parent 
                        """ left rotate fixing_node's parent. """
                        self._left_rotate(fixing_node)

                    """ Case 3). if the new node's parent's location is the left child, 
                    the parent's sibling is black, and the new node's location is the left 
                    child. """
                    fixing_node.parent.color = Color.BLACK
                    """ make fixing_node's parent/grandparent black/red. """
                    fixing_node.parent.parent.color = Color.RED 
                    """ right rotate the latter. """
                    self._right_rotate(fixing_node.parent.parent) 

            else:
                """ Case 4). if the new node's parent's location is the right child, 
                the parent's sibling is red, and the new node's doesn't matter. """
                parent_sibling = fixing_node.parent.parent.left 
                """ repeat Case 1. """
                if parent_sibling.color == Color.RED:
                    fixing_node.parent.color = Color.BLACK
                    parent_sibling.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED 
                    fixing_node = fixing_node.parent.parent

                else:
                    """ Case 5). if the new node's parent's location is the right child, 
                    the parent's sibling is black, and the new node's location is the left 
                    child. """
                    if fixing_node == fixing_node.parent.left: 
                        fixing_node = fixing_node.parent 
                        """ right rotate fixing_node's parent. """
                        self._right_rotate(fixing_node)

                    """ Case 6). if the new node's parent's location is the right child, 
                    the parent's sibling is black, and the new node's location is the right 
                    child. """
                    fixing_node.parent.color = Color.BLACK
                    """ make fixing_node's parent/grandparent black/red. """
                    fixing_node.parent.parent.color = Color.RED 
                    self._left_rotate(fixing_node.parent.parent) 

        """ while fixing the broken RBTP for fixing_node, its parent or grandparent 
        (depending on the case) may violate the RBTP. In this case, make one of these
        the new fixing_node. Then, it can be solved according to the six cases. Repeat 
        this step until the root is reached; if it becomes red (violating RBTP 1) 
        after the fix operations, make it black. """
        self.root.color = Color.BLACK

    """ To fix RBTP 4, pretend fixing_node has one extra black or red. Thus, if the node 
    to be deleted has < two children, it becomes 'double-black' or 'red-and-black' (2 or 
    1 height) after _transplant() is used to replace a node. If the node to be deleted 
    has two children, the leftmost node's replacement becomes double-black or red-and-black 
    when _transplant() is used to remove the leftmost node of the subtree. """
    def _delete_fixup(self, fixing_node: Union[Leaf, Node]) -> None:
        continue_fixing = True
        while fixing_node is not self.root and fixing_node.color == Color.BLACK and continue_fixing:
            if fixing_node == fixing_node.parent.left: 
                sibling = fixing_node.parent.right 

                """ Case 1). if fixing_node is a left child, its sibling is red, 
                and both of its sibling's childrens' colours don't matter. """
                if sibling.color == Color.RED:
                    """ make the sibling node and fixing_node's parent black and red, 
                    left rotate fixing_node's parent, and update the sibling node. """
                    fixing_node.parent.color = Color.RED 
                    self._left_rotate(fixing_node.parent) 
                    sibling = fixing_node.parent.right 

                if isinstance(sibling, Leaf):
                    continue_fixing = False

                elif sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
                    """ Case 2). if fixing_node is a left child, and its sibling and both 
                    of its children are black. """
                    sibling.color = Color.RED
                    """ make the sibling red and move fixing_node up (the new fixing_node 
                    becomes the original's parent). """
                    fixing_node = fixing_node.parent 

                else:
                    """ Case 3). if fixing_node is a left child, its sibling is black, 
                    and the sibling's left/right child is red/black. """
                    if sibling.right.color == Color.BLACK:
                        """ make the sibling/its left child red/black, and right rotate 
                        the sibling node. """
                        if sibling.left.color is not Color.BLACK:
                            sibling.left.color = Color.BLACK 
                        sibling.color = Color.RED 
                        self._right_rotate(node_x=sibling) 

                    """ Case 4). if fixing_node is a left child, its sibling is black, 
                    and its left/right child is black/red. """
                    sibling.color = fixing_node.parent.color 
                    """ make the sibling the same colour as fixing_node's parent,
                    the fixing_node‘s parent black, and sibling node's right child 
                    black. Left rotate fixing_node's parent; after these operations, 
                    all violated red-black-tree-property are restored. """
                    if fixing_node.parent.color is not Color.BLACK: 
                        fixing_node.parent.color = Color.BLACK 
                    if sibling.right.color is not Color.BLACK:
                        sibling.right.color = Color.BLACK 
                    self._left_rotate(node_x=fixing_node.parent) 
                    fixing_node = self.root

            else:
                """ Case 5). if fixing_node is a right child, its sibling is red, 
                and both of its sibling's childrens' colours don't matter. """
                sibling = fixing_node.parent.left
                """ make the sibling node and fixing_node's parent black and red, 
                right rotate fixing_node's parent, and update the sibling node. """
                if sibling.color == Color.RED:
                    fixing_node.parent.color = Color.RED 
                    self._right_rotate(node_x=fixing_node.parent) 
                    sibling = fixing_node.parent.left 

                if isinstance(sibling, Leaf):
                    continue_fixing = False

                elif sibling.right.color == Color.BLACK and sibling.left.color == Color.BLACK:
                    """ Case 6). if fixing_node is a right child, and its sibling and both 
                    of its children are black. """
                    sibling.color = Color.RED
                    """ make the sibling red and move fixing_node up. """
                    fixing_node = fixing_node.parent

                else:
                    """ Case 7). if fixing_node is a right child, its sibling is black, 
                    and its left/right child is black/red. """
                    if sibling.left.color == Color.BLACK:
                        """ make the sibling and its right child red/black, and left 
                        rotate the left sibling. """
                        if sibling.right.color is not Color.BLACK:
                            sibling.right.color = Color.BLACK
                        sibling.color = Color.RED
                        self._left_rotate(node_x=sibling)  

                    """ Case 8). if fixing_node is a right child, its sibling is black, 
                    and its left/right child is red/black. """
                    sibling.color = fixing_node.parent.color
                    """ make the sibling the same colour as fixing_node's parent,
                    the fixing_node‘s parent black, and sibling node's left child 
                    black. Right rotate fixing_node's parent. """
                    if fixing_node.parent.color is not Color.BLACK:
                        fixing_node.parent.color = Color.BLACK
                    if sibling.left.color is not Color.BLACK:
                        sibling.left.color = Color.BLACK
                    self._right_rotate(node_x=fixing_node.parent)
                    fixing_node = self.root

            if fixing_node.color is not Color.BLACK:
                fixing_node.color = Color.BLACK

    def _transplant(self, deleting_node: Node, replacing_node: Union[Node, Leaf]) -> None:
        """ replace the subtree rooted at deleting_node with the one at replacing_node.
        After replacing_node replaces deleting_node, the latter's parent becomes the 
        former's, and deleting_node's parent has replacing_node as its child.  """
        if isinstance(deleting_node.parent, Leaf):
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node

        if isinstance(replacing_node, Node):
            replacing_node.parent = deleting_node.parent

    def _inorder_traverse(self, node: Union[Node, Leaf]) -> Iterator[tuple[Any, Any]]:
        if isinstance(node, Node):
            """ left subtree, current node, right subtree. """
            yield from self._inorder_traverse(node.left)
            yield (node.key, node.data)
            yield from self._inorder_traverse(node.right)

    def _preorder_traverse(self, node: Union[Node, Leaf]) -> Iterator[tuple[Any, Any]]:
        """ current node, left subtree, right subtree. """
        if isinstance(node, Node):
            yield (node.key, node.data)
            yield from self._preorder_traverse(node.left)
            yield from self._preorder_traverse(node.right)

    def _postorder_traverse(self, node: Union[Node, Leaf]) -> Iterator[tuple[Any, Any]]:
        if isinstance(node, Node):
            """ left subtree, right subtree, current node. """
            yield from self._postorder_traverse(node.left)
            yield from self._postorder_traverse(node.right)
            yield (node.key, node.data)
