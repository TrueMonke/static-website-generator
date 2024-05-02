import unittest

import conv_funcs
from textnode import TextNode
from leafnode import LeafNode
from text_types import *
from block_types import *

class TestConvFuncs(unittest.TestCase):
    def test_text_node_to_html_node(self):
        node1 = TextNode("This is text with a ", "text")
        node2 = TextNode("bolded", "bold")
        node3 = TextNode(" word", "italic")
        node4 = TextNode("if 2 == 2: return True ", "code")
        node5 = TextNode("google", "link", url="https://www.google.com")
        node6 = TextNode("this is an image url", "image", url="https://www.google.com")
        
        test_node_text_html = conv_funcs.text_node_to_html_node(node1)
        test_node_bold_html = conv_funcs.text_node_to_html_node(node2)
        test_node_italic_html = conv_funcs.text_node_to_html_node(node3)
        test_node_code_html = conv_funcs.text_node_to_html_node(node4)
        test_node_link_html = conv_funcs.text_node_to_html_node(node5)
        test_node_image_html = conv_funcs.text_node_to_html_node(node6)

        assert isinstance(test_node_text_html, LeafNode)
        assert isinstance(test_node_bold_html, LeafNode)
        assert isinstance(test_node_italic_html, LeafNode)
        assert isinstance(test_node_code_html, LeafNode)
        assert isinstance(test_node_link_html, LeafNode)
        assert isinstance(test_node_image_html, LeafNode)


    def test_split_nodes_delimiter(self):

        input_markdown = "This is text with a `code block` word"

        node = TextNode(input_markdown, text_type_text)

        new_nodes = conv_funcs.split_nodes_delimiter([node], "`", text_type_code)

        assert_html_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]

        assert new_nodes == assert_html_nodes


    def test_split_nodes_delimiter_no_matching_delimiter(self):

        input_markdown = "This is text with a **bolded** word**"

        node = TextNode(input_markdown, text_type_text)

        with self.assertRaises(ValueError):
             new_nodes = conv_funcs.split_nodes_delimiter([node], "**", text_type_bold)


    def test_extract_markdown_images(self):

        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) \
            and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) \
                [link](https://www.example.com)"

        extracted_images = conv_funcs.extract_markdown_images(text)

        assert_exracted_images = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                                   ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]

        assert extracted_images == assert_exracted_images


    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com), \
             ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) \
                and [another](https://www.example.com/another)"

        extracted_links = conv_funcs.extract_markdown_links(text)

        assert_exracted_links = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]

        assert extracted_links == assert_exracted_links


    def test_split_nodes_images(self):

        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) ",
            text_type_text,
        )

        new_nodes = conv_funcs.split_nodes_images([node])

        assert_html_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ]

        assert new_nodes == assert_html_nodes


    def test_split_nodes_images_tail_text(self):

        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) tail text",
            text_type_text,
        )

        new_nodes = conv_funcs.split_nodes_images([node])

        assert_html_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
            TextNode(" tail text", text_type_text),
        ]

        assert new_nodes == assert_html_nodes


    def test_split_nodes_links(self):

        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            text_type_text,
        )

        new_nodes = conv_funcs.split_nodes_links([node])

        assert_html_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode(
                "another", text_type_link, "https://www.example.com/another"
            ),
        ]

        assert new_nodes == assert_html_nodes


    def test_split_nodes_links_tail_text(self):

        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) tail text ",
            text_type_text,
        )

        new_nodes = conv_funcs.split_nodes_links([node])

        assert_html_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode(
                "another", text_type_link, "https://www.example.com/another"
            ),
            TextNode(" tail text ", text_type_text),
        ]

        assert new_nodes == assert_html_nodes


    def test_text_to_textnodes(self):

        markdown_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        test_textnodes = conv_funcs.text_to_textnodes(markdown_text)

        assert_textnodes = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]

        assert test_textnodes == assert_textnodes


    def test_text_to_textnodes_no_matching_delimiter(self):

        markdown_text = "This is **text* with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        with self.assertRaises(ValueError):
             test_textnodes = conv_funcs.text_to_textnodes(markdown_text)


    def test_markdown_to_blocks(self):
        markdown_text = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"

        test_markdown_blocks = conv_funcs.markdown_to_blocks(markdown_text)

        assert_markdown_blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]

        assert test_markdown_blocks == assert_markdown_blocks


    def test_handle_heading_block_type(self):
        
        markdown_block_heading_1 = "# here is a heading"

        markdown_block_heading_6 = "###### here is a heading"

        markdown_block_heading_7 = "####### here is not a heading"


        test_block_type_valid_1 = conv_funcs.handle_heading_block_type(markdown_block_heading_1)

        test_block_type_valid_6 = conv_funcs.handle_heading_block_type(markdown_block_heading_6)

        test_block_type_invalid_7 = conv_funcs.handle_heading_block_type(markdown_block_heading_7)


        assert test_block_type_valid_1 == block_type_heading

        assert test_block_type_valid_6 == block_type_heading

        assert test_block_type_invalid_7 == block_type_paragraph


    
    def test_handle_code_block_type(self):
        
        markdown_block_code = "```this is is a code block\nthere is code here\nhere is the end```"

        markdown_block_code_invalid = "```this is is a code block\nthere is code here\nhere is the end"


        test_block_type_valid = conv_funcs.handle_code_block_type(markdown_block_code)

        test_block_type_invalid = conv_funcs.handle_code_block_type(markdown_block_code_invalid)


        assert test_block_type_valid == block_type_code

        assert test_block_type_invalid == block_type_paragraph


    
    def test_handle_quote_block_type(self):
        
        markdown_block_quote = ">this is a quot\n>there words\n>here is the end"

        markdown_block_quote_invalid = ">this is a quot\n>there words\nhere is the end"

        
        test_block_type_valid = conv_funcs.handle_quote_block_type(markdown_block_quote)

        test_block_type_invalid = conv_funcs.handle_quote_block_type(markdown_block_quote_invalid)


        assert test_block_type_valid == block_type_quote

        assert test_block_type_invalid == block_type_paragraph

    
    def test_handle_unordered_list_block_type(self):
        
        markdown_block_unordered_list = "* this is a list\n* there are items here\n- here is an item\n* here is the end"
        
        markdown_block_unordered_list_invalid = "* this is a list\nthere are items here\n- here is an item\n* here is the end"


        test_block_type_valid = conv_funcs.handle_unordered_list_block_type(markdown_block_unordered_list)

        test_block_type_invalid = conv_funcs.handle_unordered_list_block_type(markdown_block_unordered_list_invalid)


        assert test_block_type_valid == block_type_unordered_list

        assert test_block_type_invalid == block_type_paragraph


    def test_handle_ordered_list_block_type(self):
        
        markdown_block_ordered_list = "1. this is a list\n2. there are items here\n3. here is the end"

        markdown_block_ordered_list_invalid = "1. this is a list\n5. there are items here\n3. here is the end"

        test_block_type_valid = conv_funcs.handle_ordered_list_block_type(markdown_block_ordered_list)

        test_block_type_invalid = conv_funcs.handle_ordered_list_block_type(markdown_block_ordered_list_invalid)


        assert test_block_type_valid == block_type_ordered_list

        assert test_block_type_invalid == block_type_paragraph


    def test_block_to_block_type(self):

        markdown_block_heading = "### here is a heading"
        markdown_block_code = "```this is is a code block\nthere is code here\nhere is the end```"
        markdown_block_quote = ">this is a quot\n>there words\n>here is the end"
        markdown_block_unordered_list = "* this is a list\n* there are items here\n- here is an item\n* here is the end"
        markdown_block_ordered_list = "1. this is a list\n2. there are items here\n3. here is the end"
        markdown_block_paragraph = "this is an invalid list\n2. there are items here\n3. here is the end"
    
        test_block_type_heading = conv_funcs.block_to_block_type(markdown_block_heading)
        test_block_type_code = conv_funcs.block_to_block_type(markdown_block_code)
        test_block_type_quote = conv_funcs.block_to_block_type(markdown_block_quote)
        test_block_type_unordered_list = conv_funcs.block_to_block_type(markdown_block_unordered_list)
        test_block_type_ordered_list = conv_funcs.block_to_block_type(markdown_block_ordered_list)
        test_block_type_paragraph = conv_funcs.block_to_block_type(markdown_block_paragraph)

        assert test_block_type_heading == block_type_heading
        assert test_block_type_code == block_type_code
        assert test_block_type_quote == block_type_quote
        assert test_block_type_unordered_list == block_type_unordered_list
        assert test_block_type_ordered_list == block_type_ordered_list
        assert test_block_type_paragraph == block_type_paragraph


if __name__ == "__main__":
    unittest.main()
