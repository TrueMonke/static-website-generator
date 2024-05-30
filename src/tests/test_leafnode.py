import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_creation(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        assert isinstance(node1, LeafNode)
        assert isinstance(node2, LeafNode)

    def test_eq(self):
        node = LeafNode("p", "This is a leaf node")
        node2 = LeafNode("p", "This is a leaf node")
        self.assertEqual(node, node2)

    def test_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        assert_node1_to_html = "<p>This is a paragraph of text.</p>"
        assert_node2_to_html = '<a href="https://www.google.com">Click me!</a>'

        test_node1_to_html = node1.to_html()
        test_node2_to_html = node2.to_html()

        assert test_node1_to_html == assert_node1_to_html
        assert test_node2_to_html == assert_node2_to_html

    def test_none_as_tag(self):

        node1 = LeafNode(None, "Click me!", {"href": "https://www.google.com"})

        assert_node1_to_html = "Click me!"
        test_node1_to_html = node1.to_html()

        assert node1.tag is None
        assert test_node1_to_html == assert_node1_to_html


if __name__ == "__main__":
    unittest.main()
