import unittest
from html.node import Node


class NodeCase(unittest.TestCase):
    def test_init_defaults(self):
        node = Node('my node')
        self.assertEqual(node.name, 'my node')


if __name__ == '__main__':
    unittest.main()
