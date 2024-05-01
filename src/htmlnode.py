class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        from textnode import text_to_html

        children = ""

        value = "" if self.value is None else text_to_html(self.value)
        if self.children is not None:
            for child in self.children:
                children += child.to_html()

        result = f"<{self.tag} props>{value}{children}</{self.tag}>"

        return (
            result.replace("props", self.props_to_html())
            if self.props is not None
            else result.replace(" props", "")
        )

    def props_to_html(self):
        if self.props is None:
            return ""

        html = ""
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
