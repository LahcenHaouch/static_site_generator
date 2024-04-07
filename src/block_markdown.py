import re


def markdown_to_blocks(markdown):
    stripped_markdown = markdown.strip()

    return re.split(r"\n{2,}", stripped_markdown)
