import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )

class TestParentNode(unittest.TestCase):
    def test_basic_parent_node(self):
        node = ParentNode(
            "p",
            [LeafNode(None, "Hello")]
        )
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_missing_tag_raises_error(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode(None, "Hello")])
            node.to_html()

    def test_nested_parent_nodes(self):
        child_node = ParentNode("span", [LeafNode(None, "Hello")])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>Hello</span></div>")



if __name__ == "__main__":
    unittest.main()