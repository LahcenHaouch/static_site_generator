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

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            result.append([old_node])
            continue

        is_valid, words = is_text_node_valid(old_node, delimiter, text_type)

        if not is_valid:
            raise Exception(f"Invalid text: {old_node.text}")
        else:
            result.extend(words)

    return result


def is_text_node_valid(node, delimiter, text_type):
    stack = []
    word_stack = []
    result = []

    text = node.text
    for i in range(len(text)):
        char = text[i]
        in_delimiter = len(stack) >= 1

        if char == delimiter:
            if in_delimiter:
                prev_index = stack.pop()
                result.append(TextNode(text[prev_index:i], text_type))

            else:
                stack.append(i + 1)
        else:
            if in_delimiter:
                continue
            else:
                if (
                    i + 1 >= len(text)
                    or text[i + 1] == delimiter
                    and len(word_stack) >= 1
                ):
                    prev = word_stack.pop()
                    result.append(TextNode(text[prev : i + 1], "text"))
                elif len(word_stack) == 0:
                    word_stack.append(i)

    return len(stack) == 0 and len(word_stack) == 0, result


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
