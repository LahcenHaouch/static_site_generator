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
        return "code", None

    elif is_block_quote_block(block):
        return "quote", None

    elif is_block_unordered_list(block):
        return "unordered_list", None
    elif is_block_ordered_list(block):
        return "ordered_list", None

    return "paragraph", None


def is_block_heading(block):
    if block[0] != "#":
        return False, None

    max = 7 if len(block) < 7 else len(block)

    level = 1
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
    print("quote", quote)
    return HTMLNode("blockquote", "".join(quote.split("> ")))


def list_to_html(block, list_type):
    tag = "ul"
    if list_type == "ordered_list":
        tag = "ol"

    node = HTMLNode(tag, children=[])

    lines = block.split("\n")

    for line in lines:
        node.children.append(HTMLNode("li", line[1:] if tag == "ul" else line[3:]))

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


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        is_heading, level = is_block_heading(block)

        if is_heading and level == 1:
            return block[2:]

    raise Exception("no h1 found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    file = open(from_path)
    file_content = file.read()
    template_file = open(template_path)
    template_content = template_file.read()

    content = markdown_to_html_node(file_content).to_html()
    title = extract_title(file_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", content)

    destination_file = open(dest_path, "w")
    destination_file.write(template_content)

    file.close()
    template_file.close()
    destination_file.close()
