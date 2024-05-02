from textnode import TextNode


from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


def text_node_to_html_node(text_node):

    match text_node.text_type:
        case "text":
            return LeafNode(None, value=text_node.text)
        case "bold":
            return LeafNode("b", value=text_node.text)
        case "italic":
            return LeafNode("i", value=text_node.text)
        case "code":
            return LeafNode("code", value=text_node.text)
        case "link":
            return LeafNode("a", value=text_node.text, props={"href": text_node.url})
        case "image":
            return LeafNode("img", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"TextNode of {text_node.text_type} not implemented")


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    pass


if __name__ == "__main__":

    text = "This is a text node"
    text_type = "bold"
    url = "https://www.boot.dev"

    test_node = TextNode(text, text_type, url)

    print(test_node)
