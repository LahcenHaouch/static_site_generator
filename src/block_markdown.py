import re


def markdown_to_blocks(markdown):
    stripped_markdown = markdown.strip()

    return re.split(r"\n{2,}", stripped_markdown)


def block_to_block_type(block):
    if is_block_heading(block):
        return "heading"

    elif is_block_code_block(block):
        return "code"

    elif is_block_quote_block(block):
        return "quote"

    elif is_block_unordered_list(block):
        return "unordored_list"
    elif is_block_ordered_list(block):
        return "ordered-list"

    return "paragraph"


def is_block_heading(block):
    if block[0] != "#":
        return False

    max = 7 if len(block) < 7 else len(block)

    for i in range(1, max):
        if block[i] == " ":
            return True

    return False


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

    counter = 0
    for line in lines:
        if len(line) < 2 or f"{line[0]}{line[1]}" != f"{counter}.":
            return False

        counter += 1

    return True
