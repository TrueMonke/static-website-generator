import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_creation(self):
        node1 = ParentNode("p", "This is a parent node", [LeafNode(None, "this is a leaf node")])
        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        assert isinstance(node1, ParentNode)
        assert isinstance(node2, ParentNode)

    def test_eq(self):
        node = ParentNode("p", "This is a parent node", [LeafNode(None, "this is a leaf node")])
        node2 = ParentNode("p", "This is a parent node", [LeafNode(None, "this is a leaf node")])
        self.assertEqual(node, node2)


    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        test_node_to_html = node.to_html()

        assert_node_to_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

        assert test_node_to_html == assert_node_to_html


    def test_nested_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("b", [LeafNode(None, "this is a"),
                                 LeafNode(None, " nested leaf node")]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        test_nested_node_to_html = node.to_html()

        assert_nested_node_to_html = '<p><b>Bold text</b><b>this is a nested leaf node</b><i>italic text</i>Normal text</p>'

        print("")
        print(test_nested_node_to_html)
        print(assert_nested_node_to_html)

        assert test_nested_node_to_html == assert_nested_node_to_html


    def test_nested_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("p", [LeafNode(None, "this is a"),
                                 LeafNode(None, " nested leaf node")]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
