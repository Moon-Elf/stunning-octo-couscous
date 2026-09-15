import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_init(self):
        children = [LeafNode("p", "Hello")]

        node = ParentNode(
            "div",
            children,
            {"class": "container"},
        )

        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {"class": "container"})

    def test_to_html(self):
        node = ParentNode("div", [LeafNode("p", "Hello")])

        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Hello"),
                LeafNode("p", "World"),
            ],
        )

        self.assertEqual(node.to_html(), "<div><p>Hello</p><p>World</p></div>")

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "container"},
        )

        self.assertEqual(node.to_html(), '<div class="container"><p>Hello</p></div>')

    def test_to_html_with_multiple_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {
                "class": "container",
                "id": "main",
            },
        )

        self.assertEqual(
            node.to_html(), '<div class="container" id="main"><p>Hello</p></div>'
        )

    def test_to_html_with_nested_parent(self):
        node = ParentNode(
            "div",
            [ParentNode("p", [LeafNode(None, "Hello")])],
        )

        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_with_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [ParentNode("p", [LeafNode(None, "Hello")])],
                )
            ],
        )

        self.assertEqual(node.to_html(), "<div><section><p>Hello</p></section></div>")

    def test_to_html_with_parent_and_leaf_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode("p", [LeafNode(None, "Paragraph")]),
            ],
        )

        self.assertEqual(node.to_html(), "<div><h1>Title</h1><p>Paragraph</p></div>")

    def test_to_html_without_tag(self):
        node = ParentNode(None, [LeafNode(None, "Hello")])

        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_empty_tag(self):
        node = ParentNode("", [LeafNode(None, "Hello")])

        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_without_children(self):
        node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_empty_children(self):
        node = ParentNode("div", [])

        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_no_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "Hello")],
            None,
        )

        self.assertEqual(node.to_html(), "<div>Hello</div>")

    def test_to_html_with_empty_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "Hello")],
            {},
        )

        self.assertEqual(node.to_html(), "<div>Hello</div>")

    def test_repr(self):
        child = LeafNode("p", "Hello")

        node = ParentNode(
            "div",
            [child],
            {"class": "container"},
        )

        expected = (
            "tag\t\t: div\n"
            "value\t: None\n"
            "children:\n"
            "    tag\t\t: p\n"
            "    value\t: Hello\n"
            "    props\t: None\n"
            "props\t: {'class': 'container'}"
        )

        self.assertEqual(repr(node), expected)

    def test_repr_with_multiple_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "Italic text")

        node = ParentNode(
            "p",
            [child1, child2, child3],
        )

        expected = (
            "tag\t\t: p\n"
            "value\t: None\n"
            "children:\n"
            "    tag\t\t: b\n"
            "    value\t: Bold text\n"
            "    props\t: None\n"
            "    ---\n"
            "    tag\t\t: None\n"
            "    value\t: Normal text\n"
            "    props\t: None\n"
            "    ---\n"
            "    tag\t\t: i\n"
            "    value\t: Italic text\n"
            "    props\t: None\n"
            "props\t: None"
        )

        self.assertEqual(repr(node), expected)



if __name__ == "__main__":
    unittest.main()
