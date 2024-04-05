import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
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

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is a bold **text**", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a bold ", "text"),
                TextNode("text", "bold"),
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

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            "text",
        )

        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", "text"),
                TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", "text"),
                TextNode("second image", "image", "https://i.imgur.com/3elNhQu.png"),
            ],
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            "text",
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("link", "link", "https://www.example.com"),
                TextNode(" and ", "text"),
                TextNode("another", "link", "https://www.example.com/another"),
            ],
        )

    def test_text_to_text_nodes(self):
        nodes = text_to_text_nodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        )

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode(
                    "image",
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
