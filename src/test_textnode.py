import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

if __name__ == "__main__":
    unittest.main()