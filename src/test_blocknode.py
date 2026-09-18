from blocknode import markdown_to_blocks, block_to_block_type, BlockType
import unittest


class TestBlockNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
First paragraph



Second paragraph


Third paragraph
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )

    def test_markdown_to_blocks_leading_and_trailing_whitespace(self):
        md = """

    First paragraph


    Second paragraph

    """
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
            ],
        )

    def test_markdown_to_blocks_multiline_paragraph(self):
        md = """This is the first line
This is the second line
This is the third line

This is another paragraph
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is the first line\nThis is the second line\nThis is the third line",
                "This is another paragraph",
            ],
        )

    def test_markdown_to_blocks_headings(self):
        md = """# Heading 1

## Heading 2

### Heading 3
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "## Heading 2",
                "### Heading 3",
            ],
        )

    def test_markdown_to_blocks_lists(self):
        md = """- Item one
- Item two
- Item three

1. First item
2. Second item
3. Third item
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "- Item one\n- Item two\n- Item three",
                "1. First item\n2. Second item\n3. Third item",
            ],
        )

    def test_markdown_to_blocks_code_block(self):
        md = """Here is some code:

```python
def hello():
    print("Hello")
```

That was the code.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here is some code:",
                '```python\ndef hello():\n    print("Hello")\n```',
                "That was the code.",
            ],
        )

    def test_heading_one(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.Heading)

    def test_heading_six(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.Heading)

    def test_heading_with_text(self):
        block = "### This is a heading with **bold** text"
        self.assertEqual(block_to_block_type(block), BlockType.Heading)

    def test_heading_seven_hashes_is_paragraph(self):
        block = "####### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_hash_without_space_is_paragraph(self):
        block = "#Heading"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    # -------------------------
    # Code
    # -------------------------

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.Code)

    def test_multiline_code_block(self):
        block = "```\ndef hello():\n    print('hello')\n\nhello()\n```"
        self.assertEqual(block_to_block_type(block), BlockType.Code)

    def test_code_block_with_language_is_paragraph(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_unclosed_code_block_is_paragraph(self):
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    # -------------------------
    # Quotes
    # -------------------------

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.Quote)

    def test_quote_without_space(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.Quote)

    def test_multiline_quote(self):
        block = "> First line\n> Second line\n> Third line"
        self.assertEqual(block_to_block_type(block), BlockType.Quote)

    def test_quote_with_missing_greater_than(self):
        block = "> First line\nSecond line\n> Third line"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    # -------------------------
    # Unordered lists
    # -------------------------

    def test_unordered_list(self):
        block = "- First item"
        self.assertEqual(block_to_block_type(block), BlockType.Unordered_list)

    def test_multiline_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.Unordered_list)

    def test_unordered_list_requires_space(self):
        block = "-First item\n-Second item"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_unordered_list_with_invalid_line(self):
        block = "- First item\nSecond item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    # -------------------------
    # Ordered lists
    # -------------------------

    def test_ordered_list(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.Ordered_list)

    def test_multiline_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.Ordered_list)

    def test_ordered_list_must_start_at_one(self):
        block = "2. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_ordered_list_must_increment(self):
        block = "1. First item\n2. Second item\n4. Fourth item"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_ordered_list_with_duplicate_number(self):
        block = "1. First item\n2. Second item\n2. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_ordered_list_requires_space(self):
        block = "1.First item\n2.Second item"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_ordered_list_with_invalid_line(self):
        block = "1. First item\n2. Second item\nNot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    # -------------------------
    # Paragraphs
    # -------------------------

    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_multiline_paragraph(self):
        block = "This is the first line.\nThis is the second line."
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)


if __name__ == "__main__":
    unittest.main()
