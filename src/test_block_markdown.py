import unittest

from block_markdown import markdown_to_blocks, block_to_block_type


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """

        result = markdown_to_blocks(markdown)

        print("result", result)

        self.assertEqual(
            result,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type(self):
        block = "# this is a header"
        self.assertEqual(block_to_block_type(block), "heading")

        block = "```code```"
        self.assertEqual(block_to_block_type(block), "code")

        block = ">quote"
        self.assertEqual(block_to_block_type(block), "quote")

        block = "*this a list\n*this is a list"
        self.assertEqual(block_to_block_type(block), "unordered_list")

        block = "1.this a list\n2.this is a list"
        self.assertEqual(block_to_block_type(block), "ordered_list")

        block = "this is a paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")


if __name__ == "__main__":
    unittest.main()
