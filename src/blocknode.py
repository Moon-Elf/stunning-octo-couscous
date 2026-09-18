# file: blocknode.py
import re
from enum import Enum

from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, text_node_to_html_node
from inlinenode import text_to_textnodes


class BlockType(Enum):
    Paragraph = "Paragraph"
    Heading = "Heading"
    Code = "Code"
    Quote = "Quote"
    Unordered_list = "Unordered_list"
    Ordered_list = "Ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Split a Markdown document into a list of blocks.
    """
    return [b.strip() for b in markdown.split("\n\n") if b.strip()]


def block_to_block_type(block: str) -> BlockType:
    """
    Detect which kind of block we are dealing with.
    """
    # Heading
    if re.match(r"^#{1,6} ", block):
        return BlockType.Heading

    # Code block **without** a language identifier
    lines = block.split("\n")
    if lines[0] == "```" and lines[-1] == "```":
        return BlockType.Code

    # Quote block
    if all(re.match(r"^> ?", l) for l in block.split("\n")):
        return BlockType.Quote

    # Unordered list
    if all(re.match(r"^- ", l) for l in block.split("\n")):
        return BlockType.Unordered_list

    # Ordered list
    if all(re.match(r"^\d+\. ", l) for l in block.split("\n")):
        numbers = [int(re.match(r"^(\d+)\. ", l).group(1)) for l in block.split("\n")]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.Ordered_list

    return BlockType.Paragraph


# --------------------------------------------------------------------------- #
# Helper that turns a string into a list of HTMLNodes representing inline     #
# Markdown.  It uses the already‑provided text‑to‑node conversion pipeline.   #
# --------------------------------------------------------------------------- #
def text_to_children(text: str) -> list[HTMLNode]:
    """
    Convert a raw Markdown string into a list of HTMLNode objects
    (leaf nodes).  The function is intentionally tiny – it only
    glues together the already‑available inline‑markdown logic.
    """
    inline_nodes: list[TextNode] = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in inline_nodes]


# --------------------------------------------------------------------------- #
# Main conversion routine                                                          #
# --------------------------------------------------------------------------- #
def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Convert a *full* Markdown document into a single parent `HTMLNode`
    (a `<div>`).  Each block of Markdown becomes a child of that div.
    """
    blocks = markdown_to_blocks(markdown)
    div_children: list[HTMLNode] = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # ---------------------------------------------------------- #
        # Heading
        # ---------------------------------------------------------- #
        if block_type == BlockType.Heading:
            m = re.match(r"^(#{1,6})\s+(.*)", block)
            level = len(m.group(1))
            heading_tag = f"h{level}"
            content = m.group(2)
            div_children.append(ParentNode(heading_tag, text_to_children(content)))

        # ---------------------------------------------------------- #
        # Paragraph
        # ---------------------------------------------------------- #
        elif block_type == BlockType.Paragraph:
            # Collapse line breaks inside a paragraph into a single space
            collapsed = " ".join(block.split("\n"))
            div_children.append(ParentNode("p", text_to_children(collapsed)))

        # ---------------------------------------------------------- #
        # Code block – no inline parsing
        # ---------------------------------------------------------- #
        elif block_type == BlockType.Code:
            lines = block.split("\n")
            # Join the lines between the fences and keep the trailing newline
            inner = "\n".join(lines[1:-1]) + "\n"
            # <pre><code>…</code></pre>
            code_node = LeafNode("code", inner)
            pre_node = ParentNode("pre", [code_node])
            div_children.append(pre_node)

        # ---------------------------------------------------------- #
        # Quote – each line becomes a paragraph inside <blockquote>
        # ---------------------------------------------------------- #
        elif block_type == BlockType.Quote:
            quote_lines = [
                l.lstrip("> ").strip() for l in block.split("\n") if l.strip()
            ]
            children = [ParentNode("p", text_to_children(l)) for l in quote_lines]
            div_children.append(ParentNode("blockquote", children))

        # ---------------------------------------------------------- #
        # Unordered list
        # ---------------------------------------------------------- #
        elif block_type == BlockType.Unordered_list:
            items = []
            for line in block.split("\n"):
                content = line[2:]  # drop "- "
                items.append(ParentNode("li", text_to_children(content)))
            div_children.append(ParentNode("ul", items))

        # ---------------------------------------------------------- #
        # Ordered list
        # ---------------------------------------------------------- #
        elif block_type == BlockType.Ordered_list:
            items = []
            for line in block.split("\n"):
                content = re.sub(r"^\d+\.\s*", "", line)
                items.append(ParentNode("li", text_to_children(content)))
            div_children.append(ParentNode("ol", items))

    # Wrap everything in a single `<div>` element
    return ParentNode("div", div_children)
