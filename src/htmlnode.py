class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        html = []
        for attr, value in self.props.items():
            html.append(f'{attr}="{value}"')
        return " ".join(html)

    def __repr__(self):
        return f"tag\t\t: {self.tag}\nvalue\t: {self.value}\nchildren: {self.children}\nprops\t: {self.props}"
