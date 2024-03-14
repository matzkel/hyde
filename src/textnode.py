import re
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_to_text_node(text):
    nodes = split_nodes_delimiter([text], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("TextNode should take TextType argument")


def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split("\n"):
        result_line = line.strip() if line != '\n' else ""
        blocks.append(result_line)
    return blocks


# SUPPORTS ONLY SINGLE LEVEL OF NESTING!!!
# TODO: Add support for multiple levels of nesting
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes accepts only list object")
    
    if len(old_nodes) < 1:
        raise ValueError("old_nodes must have atleast 1 object")

    if not isinstance(text_type, TextType):
        raise TypeError("text_type accepts only TextType value")

    new_nodes = []
    for node in old_nodes:
        # If it encounters something that's not TextNode, treat it as a raw text
        if not isinstance(node, TextNode):
            node = TextNode(node, TextType.TEXT)
        
        splitted = node.text.split(delimiter)
        if len(splitted) != 3: # Closing delimiter not found or too much indentation
            new_nodes.append(node)
            continue
        
        # Fix this mess later, maybe
        new_nodes.append(TextNode(splitted[0], node.text_type, node.url))
        new_nodes.append(TextNode(splitted[1], text_type, node.url))
        new_nodes.append(TextNode(splitted[2], node.text_type, node.url))

    return new_nodes


def split_nodes_image(old_nodes):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes accepts only list object")

    if len(old_nodes) < 1:
        raise ValueError("old_nodes must have atleast 1 object")

    new_nodes = []
    for node in old_nodes:
        # If it encounters something that's not TextNode, treat it as a raw text
        if not isinstance(node, TextNode):
            node = TextNode(node, TextType.TEXT)

        images = extract_markdown_images(node.text)
        if len(images) < 1:
            new_nodes.append(node)
            continue

        text = node.text
        for image_tup in images:
            splitted = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)

            new_nodes.append(TextNode(splitted[0], node.text_type, node.url))
            new_nodes.append(TextNode(image_tup[0], TextType.IMAGE, image_tup[1]))

            text = splitted[1]
        
        if text != '':
            new_nodes.append(TextNode(text, node.text_type, node.url))
    
    return new_nodes

def split_nodes_link(old_nodes):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes accepts only list object")

    if len(old_nodes) < 1:
        raise ValueError("old_nodes must have atleast 1 object")

    new_nodes = []
    for node in old_nodes:
        # If it encounters something that's not TextNode, treat it as a raw text
        if not isinstance(node, TextNode):
            node = TextNode(node, TextType.TEXT)

        links = extract_markdown_links(node.text)
        if len(links) < 1:
            new_nodes.append(node)
            continue

        text = node.text
        for link_tup in links:
            splitted = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)

            new_nodes.append(TextNode(splitted[0], node.text_type, node.url))
            new_nodes.append(TextNode(link_tup[0], TextType.LINK, link_tup[1]))

            text = splitted[1]
    
        if text != '':
            new_nodes.append(TextNode(text, node.text_type, node.url))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
