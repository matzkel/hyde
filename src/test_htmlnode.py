import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()