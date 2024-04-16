import re

from htmlnode import HTMLNode


def markdown_to_blocks(markdown):
    stripped_markdown = markdown.strip()

    return re.split(r"\n{2,}", stripped_markdown)


def block_to_block_type(block):
    is_heading, level = is_block_heading(block)
    if is_heading:
        return "heading", level

    elif is_block_code_block(block):
        return "code"

    elif is_block_quote_block(block):
        return "quote"

    elif is_block_unordered_list(block):
        return "unordered_list"
    elif is_block_ordered_list(block):
        return "ordered_list"

    return "paragraph"


def is_block_heading(block):
    if block[0] != "#":
        return False

    max = 7 if len(block) < 7 else len(block)

    level = 0
    for i in range(1, max):
        if block[i] == " ":
            return True, level
        level += 1
    return False, None


def is_block_code_block(block):
    if len(block) < 6:
        return False

    return (
        block[0] == block[1] == block[2] == block[-1] == block[-2] == block[-3] == "`"
    )


def is_block_quote_block(block):
    lines = block.split("\n")

    for line in lines:
        if line[0] != ">":
            return False

    return True


def is_block_unordered_list(block):
    lines = block.split("\n")

    for line in lines:
        if line[0] != "*" and line[0] != "-":
            return False

    return True


def is_block_ordered_list(block):
    lines = block.split("\n")

    counter = 1
    for line in lines:
        if len(line) < 2 or f"{line[0]}{line[1]}" != f"{counter}.":
            return False

        counter += 1

    return True


def quote_to_html(quote):
    return HTMLNode("blockquote", quote[1:])


def list_to_html(block, list_type):
    tag = "ul"
    if list_type == "ordered_list":
        tag = "ol"

    node = HTMLNode(tag, children=[])

    lines = block.split("\n")

    for line in lines:
        node.children.append(HTMLNode("li", line[1:]))

    return node


def code_to_html(block):
    node = HTMLNode("pre", children=[])
    node.children.append(HTMLNode("code", block[3:-3]))

    return node


def heading_to_html(block, level):
    return HTMLNode(f"h{level}", block[level:])


def block_to_html(block):
    block_type, level = block_to_block_type(block)

    match block_type:
        case "quote":
            return quote_to_html(block)
        case "unordered_list":
            return list_to_html(block, block_type)
        case "ordered_list":
            return list_to_html(block, block_type)
        case "code":
            return code_to_html(block)
        case "heading":
            return heading_to_html(block, level)
        case _:
            return HTMLNode("p", block)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    node = HTMLNode("div", children=[])

    for block in blocks:
        node.children.append(block_to_html(block))

    return node
