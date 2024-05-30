import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("This is a html node", "test value", [], {})
        node2 = HTMLNode("This is a html node", "test value", [], {})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(
            "This is a text node",
            "bold",
            [],
            {"href": "https://www.google.com", "target": "_blank"},
        )
        props_html_value = node.props_to_html()
        assert_html_value = ' href="https://www.google.com" target="_blank"'
        assert props_html_value == assert_html_value


if __name__ == "__main__":
    unittest.main()
