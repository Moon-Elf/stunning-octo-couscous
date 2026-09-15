from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag == "img":
            if not self.props:
                raise ValueError("Image nodes must have props")

            html = f"<{self.tag}"

            if self.props:
                html += f" {self.props_to_html()}"

            html += ">"

            return html

        if not self.value:
            raise ValueError("All leaf nodes must have a value")

        if not self.tag:
            return self.value

        html = f"<{self.tag}"

        if self.props:
            html += f" {self.props_to_html()}"

        html += f">{self.value}</{self.tag}>"

        return html

    
    def __repr__(self):
        return f"tag\t\t: {self.tag}\nvalue\t: {self.value}\nprops\t: {self.props}"
