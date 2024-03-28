import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_diff(self):
        node = TextNode("This is a text node", "bold", "url")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ],
        )

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        images = extract_markdown_images(text)

        self.assertEqual(
            images,
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/dfsdkjfd.png"),
            ],
        )

    def test_extract_markdown_links(self):
        text = text = (
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        )
        links = extract_markdown_links(text)

        self.assertEqual(
            links,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
