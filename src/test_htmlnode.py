import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode("p", "Hello world", props={"class": "px-2", "id": "test"})

        self.assertEqual(node.props_to_html(), ' class="px-2" id="test"')


if __name__ == "__main__":
    unittest.main()
