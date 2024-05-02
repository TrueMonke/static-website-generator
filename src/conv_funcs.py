from textnode import TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from text_types import *
from block_types import *

import re

def text_node_to_html_node(text_node:TextNode) -> HTMLNode:

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
            return LeafNode("img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"TextNode of {text_node.text_type} not implemented")


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:str) -> list[TextNode]:
   
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            new_text = node.text.split(delimiter)

            if len(new_text) % 2 == 0:
                raise ValueError(f"No matching {delimiter} for {node}")
            else:
                for i in range(len(new_text)):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(new_text[i], node.text_type))
                    else:
                        new_nodes.append(TextNode(new_text[i], text_type))

    return new_nodes


def extract_markdown_images(input_text:str) -> list[tuple[str]]:
    
    extracted_images = []
    markdown_images_pattern = r'\!\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)'
    extracted_images = re.findall(markdown_images_pattern, input_text)

    return extracted_images


def extract_markdown_links(input_text:str) -> list[tuple[str]]:

    extracted_links = []
    markdown_links_pattern = r'(?:^|\s)(?<!\!)\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)'
    extracted_links = re.findall(markdown_links_pattern, input_text)

    return extracted_links


def split_nodes_images(old_nodes:list[TextNode]) -> list[TextNode]:
   
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            extract_links = extract_markdown_images(node.text)

            node_text = node.text

            for (alt, image) in extract_links:

                delimiter = f"![{alt}]({image})"
                new_text = node_text.split(delimiter, 1)

                if new_text[0] != "" or new_text[0] != " ":

                    new_nodes.append(TextNode(new_text[0], text_type_text))
                    new_nodes.append(TextNode(alt, text_type_image, image))
                    node_text = node_text.replace(new_text[0], "")
                    node_text = node_text.replace(delimiter, "")
                    
                else:
                    new_nodes.append(TextNode(alt, text_type_image, image))
                    node_text = node_text.replace(delimiter, "")

            if node_text.rstrip():
                new_nodes.append(TextNode(node_text, text_type_text))

    return new_nodes


def split_nodes_links(old_nodes:list[TextNode]) -> list[TextNode]:
   
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            extract_links = extract_markdown_links(node.text)

            node_text = node.text

            for (alt, link) in extract_links:

                delimiter = f"[{alt}]({link})"
                new_text = node_text.split(delimiter, 1)

                if new_text[0] != "" or new_text[0] != " ":

                    new_nodes.append(TextNode(new_text[0], text_type_text))
                    new_nodes.append(TextNode(alt, text_type_link, link))
                    node_text = node_text.replace(new_text[0], "")
                    node_text = node_text.replace(delimiter, "")
                    
                else:
                    new_nodes.append(TextNode(alt, text_type_link, link))
                    node_text = node_text.replace(delimiter, "")

            if node_text.rstrip():
                new_nodes.append(TextNode(node_text, text_type_text))

    return new_nodes


def text_to_textnodes(markdown_text:str) -> list[TextNode]:
    
    markdown_delimiters = {
        "**":   text_type_bold,
        "*":    text_type_italic,
        "`":    text_type_code,
    }
    
    new_textnodes = [TextNode(markdown_text, text_type_text)]

    for delimiter, text_type in markdown_delimiters.items():

        new_textnodes = split_nodes_delimiter(new_textnodes, delimiter, text_type)

    return split_nodes_images(split_nodes_links(new_textnodes))


def markdown_to_blocks(markdown_text:str) -> list[str]:

    markdown_blocks = []

    extracted_blocks = markdown_text.split("\n\n")

    for block in extracted_blocks:

        block = block.lstrip().rstrip()
        # block = block.lstrip().rstrip() + "\n"

        if block:
            markdown_blocks.append(block)

    return markdown_blocks


def handle_heading_block_type(markdown_block:str) -> str:

    heading_counter = 1
    
    if len(markdown_block) > 2:

        for character in markdown_block[1:]:

            if heading_counter >= 6:
                if character != " ":
                    return block_type_paragraph
                
            if character == "#":
                heading_counter+=1

            elif character == " ":
                return block_type_heading
            
            else:
                return block_type_paragraph

    return block_type_paragraph


def handle_code_block_type(markdown_block:str) -> str:

    if len(markdown_block) >= 6:

        if markdown_block[0:3] == "```" and markdown_block[-3:] == "```":
            return block_type_code

    return block_type_paragraph


def handle_quote_block_type(markdown_block:str) -> str:

    block_lines = markdown_block.split("\n")

    for line in block_lines:
        if line[0] != ">":
            return block_type_paragraph

    return block_type_quote


def handle_unordered_list_block_type(markdown_block:str) -> str:

    block_lines = markdown_block.split("\n")

    for line in block_lines:
        if len(line) > 2:
            
            if line[0:2] not in ["* ", "- "]:
                    return block_type_paragraph
            else:
                continue
        else:
            return block_type_paragraph
    
    return block_type_unordered_list


def handle_ordered_list_block_type(markdown_block:str) -> str:

    block_lines = markdown_block.split("\n")

    previous_digit = 0

    for line in block_lines:
        if len(line) > 2:

            expected_prefix = f"{previous_digit+1}."
            current_prefix = f"{line[0:2]}"

            if current_prefix != expected_prefix:
                return block_type_paragraph
            else:
                previous_digit = int(line[0])
        else:
            return block_type_paragraph
    
    return block_type_ordered_list


def block_to_block_type(markdown_block:str) -> str:

    initial_block_character = markdown_block[0]

    match initial_block_character:
        case "#":
            return handle_heading_block_type(markdown_block)
        case "`":
            return handle_code_block_type(markdown_block)
        case ">":
            return handle_quote_block_type(markdown_block)
        case "*":
            return handle_unordered_list_block_type(markdown_block)
        case "-":
            return handle_unordered_list_block_type(markdown_block)
        case _:
            if initial_block_character.isdigit():
                return handle_ordered_list_block_type(markdown_block)
            else:
                return block_type_paragraph
