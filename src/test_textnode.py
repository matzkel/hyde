import unittest

from textnode import (
    TextNode,
    TextType,

    text_to_text_node,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        other_node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, other_node)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        other_node = TextNode("This text node is different", TextType.ITALIC)
        self.assertNotEqual(node, other_node)
    
    def test_eq_urls(self):
        node = TextNode("This text node links to google", TextType.LINK, "https://google.com")
        other_node = TextNode("This text node links to google", TextType.LINK, "https://google.com")
        self.assertEqual(node, other_node)

    def test_not_eq_urls(self):
        node = TextNode("This text node links to something", TextType.LINK, "https://google.com")
        other_node = TextNode("This text node links to something", TextType.LINK, "https://youtube.com")
        self.assertNotEqual(node, other_node)

    def test_repr(self):
        node = TextNode("This is bold text node", TextType.BOLD)
        self.assertEqual(
            "TextNode(This is bold text node, TextType.BOLD, None)", repr(node)
        )

    def test_conversion(self):
        node = TextNode("This is bold text!", TextType.BOLD)
        node2 = text_node_to_html_node(node)
        self.assertEqual(
            "LeafNode(b, This is bold text!, None)", repr(node2)
        )

    def test_conversion2(self):
        node = TextNode(
            "This is a blank page!",
            TextType.IMAGE,
            "about:blank"
        )
        node2 = text_node_to_html_node(node)
        self.assertEqual(
            "LeafNode(img, None, {'src': 'about:blank', 'alt': 'This is a blank page!'})",
            repr(node2)
        )

    def test_split_nodes_delimiter(self):
        node = TextNode("This **word** is bold", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            "[TextNode(This , TextType.TEXT, None), TextNode(word, TextType.BOLD, None), TextNode( is bold, TextType.TEXT, None)]",
            repr(result)
        )

    def test_split_nodes_delimiter2(self):
        nodes = [
            TextNode("This **word** is bold", TextType.TEXT),
            "This one is just raw text"
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            "[TextNode(This , TextType.TEXT, None), TextNode(word, TextType.BOLD, None), TextNode( is bold, TextType.TEXT, None), TextNode(This one is just raw text, TextType.TEXT, None)]",
            repr(result)
        )
    
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        self.assertEqual(
            [('image', 'https://i.imgur.com/zjjcJKZ.png'), ('another', 'https://i.imgur.com/dfsdkjfd.png')],
            extract_markdown_images(text)
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            [('link', 'https://www.example.com'), ('another', 'https://www.example.com/another')],
            extract_markdown_links(text)
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT, None),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ], split_nodes_image([node])
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            TextType.TEXT
        )
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and ", TextType.TEXT, None),
                TextNode("another", TextType.LINK, "https://www.example.com/another")
            ], split_nodes_link([node])
        )

    def test_text_to_text_node(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://google.com)"
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT, None),
                TextNode("text", TextType.BOLD, None),
                TextNode(" with an ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" word and a ", TextType.TEXT, None),
                TextNode("code block", TextType.CODE, None),
                TextNode(" and an ", TextType.TEXT, None),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://google.com")
            ], text_to_text_node(text)
        )

    def test_text_to_text_node2(self):
        text = "This **word** should be bold, and this one should be *italic*! Here is the [link](https://example.com)."
        self.assertEqual(
            [
                TextNode("This ", TextType.TEXT, None),
                TextNode("word", TextType.BOLD, None),
                TextNode(" should be bold, and this one should be ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode("! Here is the ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.TEXT, None)
            ], text_to_text_node(text)
        )


if __name__ == "__main__":
    unittest.main()
