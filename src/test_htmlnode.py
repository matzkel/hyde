import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={
            "href": "https://google.com",
            "target": "_blank",
        })
        self.assertEqual(
            "href=\"https://google.com\" target=\"_blank\"", node.props_to_html()
        )
    
    def test_props_to_html2(self):
        node = HTMLNode(props={
            "src": "about:blank",
            "alt": "Blank page"
        })
        self.assertEqual(
            "src=\"about:blank\" alt=\"Blank page\"", node.props_to_html()
        )

    def test_repr(self):
        node = HTMLNode("p", "Hello, World!")
        self.assertEqual(
            "HTMLNode(\np,\nHello, World!,\nNone,\nNone\n)", repr(node)
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            "a",
            "This links to google!",
            {"href": "https://google.com"}
        )
        self.assertEqual(
            "<a href=\"https://google.com\">This links to google!</a>", node.to_html()
        )
    
    def test_to_html2(self):
        node = LeafNode("b", "This is bold text")
        self.assertEqual(
            "<b>This is bold text</b>", node.to_html()
        )

    def test_error(self):
        node = LeafNode(
            "img",
            None,
            {"src": "about:blank", "alt": "Blank page"}
        )
        self.assertRaises(ValueError, node.to_html)

    def test_raw_value(self):
        node = LeafNode(value="This is raw text")
        self.assertEqual(
            "This is raw text", node.to_html()
        )

    def test_repr(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(
            "LeafNode(\np,\nHello, World!,\nNone\n)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
