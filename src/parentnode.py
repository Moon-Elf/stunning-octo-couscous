from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a value")
        if not self.children:
            raise ValueError("All parent nodes must have at least one child")

        html = f"<{self.tag}"

        if self.props:
            html += f" {self.props_to_html()}"

        html += ">"

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html

    def __repr__(self):
        children_repr = ""

        if self.children:
            child_blocks = []

            for child in self.children:
                child_repr = "\n".join(
                    f"    {line}" for line in repr(child).splitlines()
                )
                child_blocks.append(child_repr)

            children_repr = "\n    ---\n".join(child_blocks)

        return (
            f"tag\t\t: {self.tag}\n"
            f"value\t: {self.value}\n"
            f"children:\n{children_repr}\n"
            f"props\t: {self.props}"
        )
