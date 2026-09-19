# src/test_extract_title.py
import unittest
from src.utils import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_with_whitespace(self):
        self.assertEqual(extract_title("#   Hello   "), "Hello")

    def test_multiline(self):
        md = "# Title\n\nSome body text."
        self.assertEqual(extract_title(md), "Title")

    def test_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## Not a title")

    def test_empty_markdown(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_h1_with_no_text(self):
        with self.assertRaises(ValueError):
            extract_title("#   ")

if __name__ == "__main__":
    unittest.main()
