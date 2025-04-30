from node import Node


class Tree:
    """ Tree class for binary tree """

    def __init__(self):
        """ Constructor for Tree class """
        self.root = None

    def getRoot(self):
        """ Method for get root of the tree """
        return self.root

    def add(self, data):
        """ Method for add data to the tree """
        if self.root is None:
            self.root = Node(data)
        else:
            self._add(data, self.root)

    def _add(self, data, node):
        """Method for add data to the tree

        Args:
            data (int): data to add

        Returns:
            None
        """
        if data < node.data:
            if node.left is not None:
                self._add(data, node.left)
            else:
                node.left = Node(data)
        else:
            if node.right is not None:
                self._add(data, node.right)
            else:
                node.right = Node(data)

    def find(self, data):
        """Method for find data in the tree

        Args:
            data (int): data to find

        Returns:
            Node: node with data
        """
        if self.root is not None:
            return self._find(data, self.root)
        else:
            return None

    def _find(self, data, node):
        """
        Recursively searches for a node with the specified data in a binary search tree.
        Args:
            data: The value to search for in the tree.
            node: The current node being examined.
        Returns:
            The node containing the specified data if found, otherwise None.
        Notes:
            - Assumes the tree follows binary search tree properties.
            - Traverses left if the data is less than the current node's data and the left child exists.
            - Traverses right if the data is greater than the current node's data and the right child exists.
        """

        if data == node.data:
            return node
        elif (data < node.data and node.left is not None):
            return self._find(data, node.left)
        elif (data > node.data and node.right is not None):
            return self._find(data, node.right)

    def deleteTree(self):
        """
        Deletes the entire tree by setting the root node to None.
        This effectively removes all nodes in the tree, making it empty.
        """

        self.root = None

    def printTree(self):
        """
        Prints the elements of the tree in an in-order traversal.
        This method starts the in-order traversal from the root of the tree
        and prints each node's value in ascending order. If the tree is empty,
        no output is produced.
        """

        if self.root is not None:
            self._printInorderTree(self.root)

    def _printInorderTree(self, node):
        """
        Recursively performs an in-order traversal of the binary tree starting from the given node.
        In an in-order traversal, the left subtree is visited first, followed by the current node,
        and then the right subtree. The data of each visited node is printed to the console.
        Args:
            node: The current node of the binary tree to process. It is expected to have
                  'left', 'right', and 'data' attributes.
        """

        if node is not None:
            self._printInorderTree(node.left)
            print(str(node.data) + ' ')
            self._printInorderTree(node.right)

    def _printPreorderTree(self, node):
        """
        Recursively performs a preorder traversal of the binary tree starting from the given node.
        In a preorder traversal, the current node's data is processed first, 
        followed by the left subtree, and then the right subtree.
        Args:
            node: The current node of the binary tree. It is expected to have 
                  'data', 'left', and 'right' attributes.
        Returns:
            None
        """

        if node is not None:
            print(str(node.data) + ' ')
            self._printPreorderTree(node.left)
            self._printPreorderTree(node.right)
        pass

    def _printPostorderTree(self, node):
        """
        Recursively performs a postorder traversal of the binary tree starting from the given node.
        In a postorder traversal, the left subtree is visited first, followed by the right subtree,
        and then the data of the current node is processed.
        Args:
            node: The current node of the binary tree to process. It is expected to have 'left', 'right',
                  and 'data' attributes.
        Returns:
            None
        """

        if node is not None:
            self._printPostorderTree(node.left)
            self._printPostorderTree(node.right)
            print(str(node.data) + ' ')
        pass


