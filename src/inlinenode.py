import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:

    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: {old_node}")

        for index, text in enumerate(parts):
            if not text:
                continue

            if index % 2 == 1:
                result.append(TextNode(text, text_type))
            else:
                result.append(TextNode(text, TextType.TEXT))

    return result


def extract_markdown_images(text: str) -> list[tuple]:
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    image_result = re.findall(image_pattern, text)
    return image_result


def extract_markdown_links(text: str) -> list[tuple]:
    link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    link_result = re.findall(link_pattern, text)
    return link_result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            # No images → keep the node as is.
            result.append(old_node)
            continue

        # We will rebuild the string piece‑by‑piece.
        remaining_text = old_node.text
        # Position in the remaining_text from where we start searching.
        cursor = 0

        for alt, url in images:
            # Find the start of this image in the remaining_text.
            # Use a regex to capture the exact Markdown string.
            img_markdown = f"![{alt}]({url})"
            start = remaining_text.find(img_markdown, cursor)
            if start == -1:
                # This should never happen – safety guard.
                continue

            # Text before the image becomes a TEXT node (if not empty).
            if start > cursor:
                before = remaining_text[cursor:start]
                result.append(TextNode(before, TextType.TEXT))

            # The image itself becomes an IMAGE node.
            result.append(TextNode(alt, TextType.IMAGE, url=url))

            # Move cursor past this image.
            cursor = start + len(img_markdown)

        # Any trailing text after the last image.
        if cursor < len(remaining_text):
            trailing = remaining_text[cursor:]
            result.append(TextNode(trailing, TextType.TEXT))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links:
            # No links → keep the node as is.
            result.append(old_node)
            continue

        # We will rebuild the string piece‑by‑piece.
        remaining_text = old_node.text
        # Position in the remaining_text from where we start searching.
        cursor = 0

        for alt, url in links:
            # Find the start of this LINK in the remaining_text.
            # Use a regex to capture the exact Markdown string.
            link_markdown = f"[{alt}]({url})"
            start = remaining_text.find(link_markdown, cursor)
            if start == -1:
                # This should never happen – safety guard.
                continue

            # Text before the LINK becomes a TEXT node (if not empty).
            if start > cursor:
                before = remaining_text[cursor:start]
                result.append(TextNode(before, TextType.TEXT))

            # The LINK itself becomes an LINK node.
            result.append(TextNode(alt, TextType.LINK, url=url))

            # Move cursor past this LINK.
            cursor = start + len(link_markdown)

        # Any trailing text after the last LINK.
        if cursor < len(remaining_text):
            trailing = remaining_text[cursor:]
            result.append(TextNode(trailing, TextType.TEXT))

    return result


def text_to_textnodes(text):
    # Starting with whole para as one TEXT node
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]

    # Bold - **...**
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Italic - _..._
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Code - `...`
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Image - ![alt](url)
    nodes = split_nodes_image(nodes)

    # Link - [text](url)
    nodes = split_nodes_link(nodes)

    return nodes
