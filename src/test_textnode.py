import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a different text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_dif_text_type(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)

	def test_dif_text_contenxt(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a different text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_dif_url(self):
		node = TextNode("This is a text node", TextType.LINK, "https://example.com")
		node2 = TextNode("This is a text node", TextType.LINK, "https://another-example.com")
		self.assertNotEqual(node, node2)

	def test_one_url_none(self):
		node = TextNode("This is a text node", TextType.LINK, "https://example.com")
		node2 = TextNode("This is a text node", TextType.LINK)
		self.assertNotEqual(node, node2)

if __name__ == "__main__":
	unittest.main()
