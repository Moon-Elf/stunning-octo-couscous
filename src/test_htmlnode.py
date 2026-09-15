import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()

        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_and_attributes(self):
        node = HTMLNode(
            tag="p",
            value="Hello",
            children=None,
            props={"class": "intro"},
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "intro"})

    def test_props_to_html_empty_when_props_is_none(self):
        node = HTMLNode(tag=None, value="Some", children=None, props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_when_props_is_empty_dict(self):
        node = HTMLNode(tag="span", value="text", children=None, props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_non_empty(self):
        props = {"id": "main", "data-value": "123"}
        node = HTMLNode(tag="div", value=None, children=None, props=props)
        # The order of items is preserved in Python 3.7+
        expected = 'id="main" data-value="123"'
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode(tag="div", value=None, children=None, props=None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_basic(self):
        node = HTMLNode(
            tag="a",
            value="link",
            children=None,
            props={"href": "https://example.com"},
        )
        expected_repr = (
            "tag\t\t: a\n"
            "value\t: link\n"
            "children: None\n"
            "props\t: {'href': 'https://example.com'}"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_all_none(self):
        node = HTMLNode(tag=None, value=None, children=None, props=None)
        expected_repr = (
            "tag\t\t: None\n" "value\t: None\n" "children: None\n" "props\t: None"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_children_as_list(self):
        child = HTMLNode(tag="li", value="Item", children=None, props=None)
        parent = HTMLNode(tag="ul", value=None, children=[child], props=None)
        self.assertIsInstance(parent.children, list)
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0], child)
        self.assertEqual(parent.children[0].tag, "li")
        self.assertEqual(parent.children[0].value, "Item")


if __name__ == "__main__":
    unittest.main()
