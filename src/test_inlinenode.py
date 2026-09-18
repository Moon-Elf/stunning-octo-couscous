import unittest

from textnode import TextNode, TextType
from inlinenode import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_code_delimiter(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        node = TextNode(
            "This is _italic_ text",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC,
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_text_with_multiple_delimited_sections(self):
        node = TextNode(
            "This is `code` and this is `more code`",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_delimiter_at_start(self):
        node = TextNode(
            "`code` at the beginning",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the beginning", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_delimiter_at_end(self):
        node = TextNode(
            "At the end `code`",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("At the end ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_entire_text_is_delimited(self):
        node = TextNode(
            "`code`",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = []

        self.assertEqual(result, expected)

    def test_text_without_delimiter(self):
        node = TextNode(
            "This is just normal text",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("This is just normal text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_non_text_node_is_preserved(self):
        node = TextNode(
            "already bold",
            TextType.BOLD,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("already bold", TextType.BOLD),
        ]

        self.assertEqual(result, expected)

    def test_non_text_nodes_are_not_modified(self):
        nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode("italic text", TextType.ITALIC),
            TextNode("code text", TextType.CODE),
        ]

        result = split_nodes_delimiter(
            nodes,
            "`",
            TextType.CODE,
        )

        self.assertEqual(result, nodes)

    def test_mixed_text_and_non_text_nodes(self):
        nodes = [
            TextNode("normal `code` text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("more `code`", TextType.TEXT),
        ]

        result = split_nodes_delimiter(
            nodes,
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("normal ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("more ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises_exception(self):
        node = TextNode(
            "This has `unclosed code",
            TextType.TEXT,
        )

        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [node],
                "`",
                TextType.CODE,
            )

    def test_multiple_unmatched_delimiters_raises_exception(self):
        node = TextNode(
            "This `has `multiple `unmatched",
            TextType.TEXT,
        )

        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [node],
                "`",
                TextType.CODE,
            )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("first `code`", TextType.TEXT),
            TextNode("second `code`", TextType.TEXT),
        ]

        result = split_nodes_delimiter(
            nodes,
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("first ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_empty_delimited_content(self):
        node = TextNode(
            "This is `` empty code",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode(" empty code", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_extract_single_image(self):
        text = "This is a Potato and it looks like ![A Potato](www.test.com/potato.jpg)"

        result = extract_markdown_images(text)

        expected = [("A Potato", "www.test.com/potato.jpg")]

        self.assertEqual(result, expected)

    def test_extract_multiple_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        result = extract_markdown_images(text)

        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

        self.assertEqual(result, expected)

    def test_extract_image_amd_link(self):
        text = "This is a Potato and it looks like ![A Potato](www.test.com/potato.jpg) and click here to see [A Potato](www.test.com/potato.jpg)"

        result = extract_markdown_images(text)

        expected = [("A Potato", "www.test.com/potato.jpg")]

        self.assertEqual(result, expected)

    def test_extract_image_only_link(self):
        text = (
            "This is a Potato and click here to see [A Potato](www.test.com/potato.jpg)"
        )

        result = extract_markdown_images(text)

        expected = []

        self.assertEqual(result, expected)

    def test_extract_single_link(self):
        text = (
            "This is a Potato and click here to see [A Potato](www.test.com/potato.jpg)"
        )

        result = extract_markdown_links(text)

        expected = [("A Potato", "www.test.com/potato.jpg")]

        self.assertEqual(result, expected)

    def test_extract_multiple_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        result = extract_markdown_links(text)

        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertEqual(result, expected)

    def test_extract_link_amd_image(self):
        text = "This is a Potato and it looks like ![A Potato](www.test.com/potato.jpg) and click here to see [A Potato](www.test.com/potato.jpg)"

        result = extract_markdown_links(text)

        expected = [("A Potato", "www.test.com/potato.jpg")]

        self.assertEqual(result, expected)

    def test_extract_link_only_image(self):
        text = "This is a Potato and it looks like ![A Potato](www.test.com/potato.jpg)"

        result = extract_markdown_links(text)

        expected = []

        self.assertEqual(result, expected)

    def test_extract_image_with_empty_alt_text(self):
        text = "![ ](image.jpg)"

        result = extract_markdown_images(text)

        expected = [(" ", "image.jpg")]

        self.assertEqual(result, expected)

    def test_extract_link_with_empty_text(self):
        text = "[](https://example.com)"

        result = extract_markdown_links(text)

        expected = [("", "https://example.com")]

        self.assertEqual(result, expected)

    def test_extract_image_with_empty_url(self):
        text = "![](image.jpg)"

        result = extract_markdown_images(text)

        expected = [("", "image.jpg")]

        self.assertEqual(result, expected)

    def test_extract_multiple_images_and_links(self):
        text = (
            "![one](one.jpg) "
            "[first](one.com) "
            "![two](two.jpg) "
            "[second](two.com)"
        )

        self.assertEqual(
            extract_markdown_images(text), [("one", "one.jpg"), ("two", "two.jpg")]
        )

        self.assertEqual(
            extract_markdown_links(text), [("first", "one.com"), ("second", "two.com")]
        )

    def test_extract_image_does_not_extract_link(self):
        text = "[Potato](potato.jpg)"

        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_link_does_not_extract_image(self):
        text = "![Potato](potato.jpg)"

        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_link_after_exclamation_mark(self):
        text = "Wow! [Potato](potato.jpg)"

        result = extract_markdown_links(text)

        expected = [("Potato", "potato.jpg")]

        self.assertEqual(result, expected)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_image_no_image(self):
        node = TextNode("Just some plain text.", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [TextNode("Just some plain text.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_image_only_image(self):
        node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                )
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/image.png) some text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
                TextNode(" some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "some text ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("some text ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_split_image_multiple_images(self):
        node = TextNode(
            "![one](https://example.com/1.png)"
            "middle"
            "![two](https://example.com/2.png)"
            "end"
            "![three](https://example.com/3.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("middle", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
                TextNode("end", TextType.TEXT),
                TextNode("three", TextType.IMAGE, "https://example.com/3.png"),
            ],
            new_nodes,
        )

    def test_split_image_adjacent_images(self):
        node = TextNode(
            "![one](https://example.com/1.png)![two](https://example.com/2.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
            ],
            new_nodes,
        )

    def test_split_image_preserves_non_text_nodes(self):
        text_node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.TEXT,
        )
        image_node = TextNode(
            "already an image",
            TextType.IMAGE,
            "https://example.com/existing.png",
        )

        new_nodes = split_nodes_image([text_node, image_node])

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(
                    "already an image",
                    TextType.IMAGE,
                    "https://example.com/existing.png",
                ),
            ],
            new_nodes,
        )

    def test_split_image_empty_text(self):
        node = TextNode("", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [TextNode("", TextType.TEXT)],
            new_nodes,
        )

    def test_split_link_no_link(self):
        node = TextNode("Just some plain text.", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [TextNode("Just some plain text.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_link_only_link(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                )
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev) is a website",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" is a website", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_split_link_multiple_links(self):
        node = TextNode(
            "[Boot](https://www.boot.dev) and "
            "[YouTube](https://www.youtube.com) and "
            "[GitHub](https://github.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Boot", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
            ],
            new_nodes,
        )

    def test_split_link_adjacent_links(self):
        node = TextNode(
            "[one](https://example.com/1)[two](https://example.com/2)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "https://example.com/1"),
                TextNode("two", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )

    def test_split_link_preserves_non_text_nodes(self):
        text_node = TextNode(
            "[link](https://example.com)",
            TextType.TEXT,
        )
        image_node = TextNode(
            "an image",
            TextType.IMAGE,
            "https://example.com/image.png",
        )

        new_nodes = split_nodes_link([text_node, image_node])

        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(
                    "an image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_split_link_empty_text(self):
        node = TextNode("", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [TextNode("", TextType.TEXT)],
            new_nodes,
        )

    def test_split_image_duplicate_images(self):
        node = TextNode(
            "![image](https://example.com/a.png) "
            "![image](https://example.com/a.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/a.png"),
            ],
            new_nodes,
        )

    def test_split_link_duplicate_links(self):
        node = TextNode(
            "[click](https://example.com) " "[click](https://example.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("click", TextType.LINK, "https://example.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("click", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
