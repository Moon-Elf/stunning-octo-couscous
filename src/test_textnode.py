import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):

    def test_equal_text_nodes(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node1, node2)

    def test_not_equal_different_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)

        self.assertNotEqual(node1, node2)

    def test_not_equal_different_text(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("World", TextType.TEXT)

        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        node1 = TextNode("Google", TextType.LINK, "https://google.com")
        node2 = TextNode("Google", TextType.LINK, "https://example.com")

        self.assertNotEqual(node1, node2)

    def test_default_url_is_none(self):
        node = TextNode("Hello", TextType.TEXT)

        self.assertIsNone(node.url)

    def test_text(self):
        node = TextNode("Hello world", TextType.TEXT)

        self.assertEqual(node.text, "Hello world")

    def test_text_type(self):
        node = TextNode("Hello world", TextType.BOLD)

        self.assertEqual(node.text_type, TextType.BOLD)

    def test_url(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")

        self.assertEqual(node.url, "https://google.com")

    def test_not_equal_to_non_textnode(self):
        node = TextNode("Hello", TextType.TEXT)

        self.assertNotEqual(node, "Hello")

    def test_repr(self):
        node = TextNode("Hello", TextType.BOLD)

        self.assertEqual(repr(node), "TextNode(Hello, bold, None)")


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        text_node = TextNode("Hello world", TextType.TEXT)

        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello world")
        self.assertIsNone(html_node.props)

        self.assertEqual(html_node.to_html(), "Hello world")

    def test_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)

        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)

        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)

        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code(self):
        text_node = TextNode("print('Hello')", TextType.CODE)

        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")
        self.assertIsNone(html_node.props)

        self.assertEqual(
            html_node.to_html(),
            "<code>print('Hello')</code>",
        )

    def test_link(self):
        text_node = TextNode(
            "Google",
            TextType.LINK,
            "https://google.com",
        )

        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(
            html_node.props,
            {"href": "https://google.com"},
        )

        self.assertEqual(
            html_node.to_html(),
            '<a href="https://google.com">Google</a>',
        )

    def test_image(self):
        text_node = TextNode(
            "A picture",
            TextType.IMAGE,
            "https://example.com/image.png",
        )

        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/image.png",
                "alt": "A picture",
            },
        )

        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/image.png" alt="A picture">',
        )


if __name__ == "__main__":
    unittest.main()
