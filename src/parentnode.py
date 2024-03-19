from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")

        if self.children is None:
            raise ValueError("Missing children")

        value = []

        for child in self.children:
            value.append(child.to_html())

        value = "".join(value)

        return f"<{self.tag}{self.props_to_html()}>{value}</{self.tag}>"
