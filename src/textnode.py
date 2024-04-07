import re

from leafnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case "image":
            return LeafNode(
                tag="img",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise Exception("WTF man!")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        if len(node.text) == 0:
            continue

        if (not isinstance(node, TextNode)) or (
            isinstance(node, TextNode) and node.text_type != "text"
        ):
            result.append(node)
            continue

        node_texts = node.text.split(delimiter)

        if len(node_texts) % 2 == 0:
            raise Exception(f"Invalid text: {node.text}")

        for i in range(len(node_texts)):
            if len(node_texts[i]) == 0:
                continue
            if i % 2 != 0:

                result.append(TextNode(node_texts[i], text_type))
            else:
                result.append(TextNode(node_texts[i], "text"))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
        else:
            text_to_split = node.text
            for image in images:
                text_split = text_to_split.split(f"![{image[0]}]({image[1]})")
                new_nodes.append(TextNode(text_split[0], "text"))
                new_nodes.append(TextNode(image[0], "image", image[1]))
                text_to_split = text_split[1]

            if len(text_to_split) > 0:
                new_nodes.append(TextNode(text_to_split, "text"))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
        else:
            text_to_split = node.text
            for link in links:
                text_split = text_to_split.split(f"[{link[0]}]({link[1]})")
                new_nodes.append(TextNode(text_split[0], "text"))
                new_nodes.append(TextNode(link[0], "link", link[1]))
                text_to_split = text_split[1]

    return new_nodes


def text_to_text_nodes(text):
    with_code_nodes = split_nodes_delimiter([TextNode(text, "text")], "`", "code")
    with_bold_nodes = split_nodes_delimiter(with_code_nodes, "**", "bold")
    with_italic_nodes = split_nodes_delimiter(with_bold_nodes, "*", "italic")
    with_images = split_nodes_image(with_italic_nodes)
    return split_nodes_link(with_images)
