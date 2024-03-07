import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()