import unittest

from tree import Tree
from node import Node

class TestTreeFind(unittest.TestCase):
    def setUp(self):
        # Create a tree and add some values for testing
        self.tree = Tree()
        for value in [10, 5, 15, 3, 7, 12, 18]:
            self.tree.add(value)

    def test_find_existing_node(self):
        """
        Test that finding an existing value returns a Node with correct data.
        """
        # Find a value that is in the tree
        node = self.tree.find(7)
        # Ensure a node is returned and it's the correct one
        self.assertIsNotNone(node, "Expected to find node with data 7, but got None.")
        self.assertIsInstance(node, Node, "Expected returned object to be an instance of Node.")
        self.assertEqual(node.data, 7, "Expected node.data to be 7.")

    def test_find_nonexistent_node(self):
        """
        Test that finding a value not in the tree returns None.
        """
        # Try to find a value that is not in the tree
        node = self.tree.find(999)
        # Ensure None is returned for non-existing value
        self.assertIsNone(node, "Expected None when searching for a non-existent value.")

if __name__ == '__main__':
    unittest.main()
