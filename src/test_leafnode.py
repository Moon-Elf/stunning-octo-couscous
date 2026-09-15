import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_init(self):
        node = LeafNode("p", "Hello", {"class": "intro"})

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "intro"})

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_without_tag(self):
        node = LeafNode(None, "This is raw text.")

        self.assertEqual(node.to_html(), "This is raw text.")

    def test_to_html_without_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_empty_value(self):
        node = LeafNode("p", "")

        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("p", "Hello", {"class": "intro"})

        expected = "tag\t\t: p\n" "value\t: Hello\n" "props\t: {'class': 'intro'}"

        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
