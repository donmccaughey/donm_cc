import unittest

from markup.node import Node, with_node


class NodeTestCase(unittest.TestCase):
    def test_init_defaults(self):
        node = Node('my node')
        self.assertEqual(node.name, 'my node')
        self.assertEqual(node.children, [])
        self.assertIsNone(node.next_sibling)
        self.assertIsNone(node.parent)
        self.assertIsNone(node.previous_sibling)

    def test_init_with_parent(self):
        parent = Node('parent')
        child = Node('child', parent)

        self.assertEqual(parent.children, [child])

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.parent, parent)

    def test_init_parent_set_from_with_node(self):
        parent = Node('parent')
        with_node.append(parent)

        child = Node('child')

        self.assertEqual(parent.children, [child])

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.parent, parent)

    def test_init_parent_from_context_handler(self):
        parent = Node('parent')

        self.assertEqual(with_node, [None])
        with parent:
            self.assertEqual(with_node, [None, parent])
            child = Node('child')
        self.assertEqual(with_node, [None])

        self.assertEqual(parent.children, [child])

        self.assertEqual(child.name, 'child')
        self.assertEqual(child.parent, parent)

    def test_has_children(self):
        parent = Node('parent')
        self.assertFalse(parent.has_children)

        Node('child', parent)
        self.assertTrue(parent.has_children)

    def test_attach(self):
        parent = Node('parent')
        child1 = Node('child1')
        child2 = Node('child2')

        child1.attach(parent)
        self.assertEqual(child1.parent, parent)
        self.assertIsNone(child1.previous_sibling)
        self.assertIsNone(child1.next_sibling)

        self.assertEqual(parent.children, [child1])

        child2.attach(parent)
        self.assertEqual(child2.parent, parent)
        self.assertEqual(child2.previous_sibling, child1)
        self.assertIsNone(child2.next_sibling)

        self.assertEqual(child1.next_sibling, child2)

        self.assertEqual(parent.children, [child1, child2])

    def test_attach_children(self):
        parent = Node('parent')
        child1 = Node('child1')
        child2 = Node('child2')

        parent.attach_children([child1, child2])

        self.assertEqual(parent.children, [child1, child2])
        self.assertEqual(child1.parent, parent)
        self.assertEqual(child2.parent, parent)

        self.assertIsNone(child1.previous_sibling)
        self.assertEqual(child1.next_sibling, child2)

        self.assertEqual(child2.previous_sibling, child1)
        self.assertIsNone(child2.next_sibling)

    def test_detach_children(self):
        parent = Node('parent')
        with parent:
            child1 = Node('child1')
            child2 = Node('child2')

        detached = parent.detach_children()

        self.assertEqual([], parent.children)
        self.assertEqual([child1, child2], detached)

        self.assertIsNone(child1.parent)
        self.assertIsNone(child2.parent)

    def test_detach_children_when_empty(self):
        parent = Node('parent')

        detached = parent.detach_children()

        self.assertEqual([], parent.children)
        self.assertEqual([], detached)

    def test_detach_descendants(self):
        parent = Node('parent')
        with parent:
            child1 = Node('child1')
            with child1:
                grandchild1 = Node('grandchild1')
                grandchild2 = Node('grandchild2')
            child2 = Node('child2')

        detached = parent.detach_descendants(lambda node: node.name.startswith('g'))

        self.assertEqual([child1, child2], parent.children)
        self.assertEqual([], child1.children)
        self.assertEqual([], child2.children)
        self.assertEqual([grandchild1, grandchild2], detached)

        self.assertIsNone(grandchild1.parent)
        self.assertIsNone(grandchild2.parent)


if __name__ == '__main__':
    unittest.main()