# src/utils.py
from pathlib import Path
from typing import Union

from blocknode import markdown_to_html_node


# --------------------------------------------------------------------------- #
# 1️⃣  extract_title
# --------------------------------------------------------------------------- #
def extract_title(markdown: Union[str, Path]) -> str:
    """
    Pull the first level‑1 heading from a Markdown string.

    Parameters
    ----------
    markdown : str | Path
        Either the raw Markdown text or a Path to a .md file.

    Returns
    -------
    str
        The title text (no leading ‘#’, no surrounding whitespace).

    Raises
    ------
    ValueError
        If no `# …` header is found, or the header contains no text.
    """
    if isinstance(markdown, Path):
        markdown = markdown.read_text(encoding="utf-8")

    for raw_line in markdown.splitlines():
        line = raw_line.lstrip()  # ignore leading spaces
        if line.startswith("#") and not line.startswith("##"):
            # strip the first ‘#’ and any whitespace after it
            title = line[1:].strip()
            if title:
                return title
            else:
                raise ValueError("H1 header is empty")
    raise ValueError("No H1 header found in markdown")


# --------------------------------------------------------------------------- #
# 2️⃣  generate_page
# --------------------------------------------------------------------------- #
def generate_page(
    from_path: str | Path,
    template_path: str | Path,
    dest_path: str | Path,
    basepath: str = "/",
) -> None:
    """
    Read a Markdown file, convert it to HTML, pull the title, fill a template
    and write the final page to *dest_path*.

    The function prints a short status message so you can see what is happening.
    """

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 1️⃣  Read the source files
    markdown = Path(from_path).read_text(encoding="utf-8")
    template = Path(template_path).read_text(encoding="utf-8")

    # 2️⃣  Convert Markdown → HTML node tree
    #      (import lazily to avoid a circular import with src.main)
    # <-- adjust if the function lives elsewhere
    root_node = markdown_to_html_node(markdown)
    html_content = root_node.to_html()

    # 3️⃣  Grab the title from the Markdown
    title = extract_title(markdown)

    # 4️⃣  Replace placeholders in the template
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    # 5️⃣  Write out the final page (create dirs if needed)
    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    Path(dest_path).write_text(page, encoding="utf-8")


def generate_pages_recursive(
    dir_path_content: str | Path,
    template_path: str | Path,
    dest_dir_path: str | Path,
    basepath: str = "/",
) -> None:
    """Generate HTML pages for every Markdown file under a content directory."""
    content_root = Path(dir_path_content)
    destination_root = Path(dest_dir_path)

    if not content_root.is_dir():
        raise FileNotFoundError(f"Content directory '{content_root}' does not exist")

    for source_path in content_root.rglob("*.md"):
        relative_path = source_path.relative_to(content_root).with_suffix(".html")
        destination_path = destination_root / relative_path
        generate_page(source_path, template_path, destination_path, basepath)
