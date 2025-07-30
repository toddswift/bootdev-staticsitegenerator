import unittest 
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "Content", {"class": "test"})
        node2 = HTMLNode("div", "Content", {"class": "test"})
        self.assertEqual(node, node2)

    def test_not_eq_tag(self):
        node = HTMLNode("div", "Content")
        node2 = HTMLNode("span", "Content")
        self.assertNotEqual(node, node2)

    def test_not_eq_value(self):
        node = HTMLNode("div", "Content")
        node2 = HTMLNode("div", "Different Content")
        self.assertNotEqual(node, node2)

    def test_not_eq_props(self):
        node = HTMLNode("div", "Content", props={"class": "test"})

    def test_init_with_all_parameters(self):
        node = HTMLNode(tag="div", value="Hello", children=["child1", "child2"], props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(node.props, {"class": "container"})

    def test_init_with_default_parameters(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_init_with_empty_children(self):
        node = HTMLNode(tag="p", value="Text", children=None)
        self.assertEqual(node.children, [])

    def test_init_with_empty_props(self):
        node = HTMLNode(tag="p", value="Text", props=None)
        self.assertEqual(node.props, {})

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"id": "main"})
        self.assertEqual(node.props_to_html(), ' id="main"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"class": "btn", "id": "submit", "data-test": "value"})
        expected = ' class="btn" id="submit" data-test="value"'
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(tag="a", value="Link", children=["child"], props={"href": "#"})
        expected = "HTMLNode(tag=a, value=Link, props={'href': '#'}, children=['child'])"
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_init_no_tag_no_props(self):
        node = LeafNode(value="Hello")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, {})
        self.assertEqual(node.children, [])

    def test_init_with_tag_and_props(self):
        props = {"class": "text-bold", "id": "main"}
        node = LeafNode(tag="p", value="Paragraph", props=props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Paragraph")
        self.assertEqual(node.props, props)
        self.assertEqual(node.children, [])

    def test_to_html_no_tag(self):
        node = LeafNode(value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_with_tag_no_props(self):
        node = LeafNode(tag="span", value="Inline text")
        self.assertEqual(node.to_html(), "<span>Inline text</span>")

    def test_to_html_with_tag_and_props(self):
        props = {"class": "link", "href": "https://example.com"}
        node = LeafNode(tag="a", value="Click me", props=props)
        self.assertEqual(node.to_html(), '<a class="link" href="https://example.com">Click me</a>')

    def test_to_html_missing_value(self):
        node = LeafNode(tag="div")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Leaf nodes must have a value.")

    def test_to_html_empty_value(self):
        node = LeafNode(tag="p", value="")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Leaf nodes must have a value.")

class TestParentNode(unittest.TestCase):
    def test_init_with_valid_input(self):
        """Test initialization with valid tag, children, and props."""
        leaf = LeafNode(tag="p", value="Text")
        parent = ParentNode(tag="div", children=[leaf], props={"class": "container"})
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [leaf])
        self.assertEqual(parent.props, {"class": "container"})
        self.assertEqual(parent.value, None)  # Inherited from HTMLNode

    def test_init_with_no_props(self):
        """Test initialization with no props (defaults to empty dict)."""
        leaf = LeafNode(tag="p", value="Text")
        parent = ParentNode(tag="div", children=[leaf])
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [leaf])
        self.assertEqual(parent.props, {})

    def test_to_html_single_child(self):
        """Test to_html with a single child node."""
        leaf = LeafNode(tag="p", value="Hello")
        parent = ParentNode(tag="div", children=[leaf])
        expected = "<div><p>Hello</p></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_multiple_children(self):
        """Test to_html with multiple child nodes."""
        leaf1 = LeafNode(tag="p", value="First")
        leaf2 = LeafNode(tag="span", value="Second")
        parent = ParentNode(tag="div", children=[leaf1, leaf2])
        expected = "<div><p>First</p><span>Second</span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_props(self):
        """Test to_html with properties."""
        leaf = LeafNode(tag="p", value="Text")
        parent = ParentNode(tag="div", children=[leaf], props={"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><p>Text</p></div>'
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_nested_parent(self):
        """Test to_html with nested ParentNode."""
        leaf = LeafNode(tag="span", value="Nested")
        inner_parent = ParentNode(tag="p", children=[leaf])
        outer_parent = ParentNode(tag="div", children=[inner_parent])
        expected = "<div><p><span>Nested</span></p></div>"
        self.assertEqual(outer_parent.to_html(), expected)

    def test_to_html_no_tag_raises_error(self):
        """Test to_html raises ValueError when tag is None."""
        leaf = LeafNode(tag="p", value="Text")
        parent = ParentNode(tag=None, children=[leaf])
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "Parent nodes must have a tag.")

    def test_to_html_no_children_raises_error(self):
        """Test to_html raises ValueError when children is empty."""
        parent = ParentNode(tag="div", children=[])
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "Parent nodes must have children.")

    def test_to_html_none_children_raises_error(self):
        """Test to_html raises ValueError when children is None."""
        parent = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "Parent nodes must have children.")

    def test_to_html_child_raises_error(self):
        """Test to_html propagates errors from child nodes."""
        leaf = LeafNode(tag="p", value=None)  # Invalid LeafNode with no value
        parent = ParentNode(tag="div", children=[leaf])
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "Leaf nodes must have a value.")

    def test_eq_same_nodes(self):
        """Test equality comparison between identical ParentNodes."""
        leaf1 = LeafNode(tag="p", value="Text")
        leaf2 = LeafNode(tag="p", value="Text")
        parent1 = ParentNode(tag="div", children=[leaf1], props={"class": "test"})
        parent2 = ParentNode(tag="div", children=[leaf2], props={"class": "test"})
        self.assertEqual(parent1, parent2)

    def test_eq_different_nodes(self):
        """Test inequality when nodes differ."""
        leaf1 = LeafNode(tag="p", value="Text")
        leaf2 = LeafNode(tag="span", value="Text")
        parent1 = ParentNode(tag="div", children=[leaf1])
        parent2 = ParentNode(tag="div", children=[leaf2])
        self.assertNotEqual(parent1, parent2)

    def test_repr(self):
        """Test string representation of ParentNode."""
        leaf = LeafNode(tag="p", value="Text")
        parent = ParentNode(tag="div", children=[leaf], props={"class": "test"})
        expected = f"HTMLNode(tag=div, value=None, props={{'class': 'test'}}, children=[{repr(leaf)}])"
        self.assertEqual(repr(parent), expected)

if __name__ == '__main__':
    unittest.main()