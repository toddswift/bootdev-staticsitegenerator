import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_multiple_images(self):
        matches = extract_markdown_images(
            "Text ![alt1](url1.jpg) more text ![alt2](url2.png)"
        )
        self.assertListEqual([("alt1", "url1.jpg"), ("alt2", "url2.png")], matches)
    
    def test_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)
    
    def test_no_images(self):
        matches = extract_markdown_images("This is plain text without images")
        self.assertListEqual([], matches)
    
    def test_empty_alt_text(self):
        matches = extract_markdown_images("![](/image.png)")
        self.assertListEqual([("", "/image.png")], matches)
    
    def test_special_characters(self):
        matches = extract_markdown_images(
            "![alt with spaces & special chars!](http://example.com/image with spaces.jpg?query=1)"
        )
        self.assertListEqual(
            [("alt with spaces & special chars!", "http://example.com/image with spaces.jpg?query=1")],
            matches
        )
    
    #def test_invalid_syntax(self):
    #    matches = extract_markdown_images("![alt text(url) or [alt](url) or !(alt)[url]")
    #    self.assertListEqual([], matches)
    
    def test_mixed_valid_invalid(self):
        matches = extract_markdown_images(
            "![valid](url1.jpg) invalid ![alt](url2.png) ![] [alt](url)"
        )
        self.assertListEqual([("valid", "url1.jpg"), ("alt", "url2.png")], matches)
    
    def test_whitespace(self):
        matches = extract_markdown_images("  ![  alt text  ](  url3.gif  )  ")
        self.assertListEqual([("  alt text  ", "  url3.gif  ")], matches)
    
    #def test_nested_brackets(self):
    #    matches = extract_markdown_images("![alt [nested] text](url4.jpg)")
    #    self.assertListEqual([("alt [nested] text", "url4.jpg")], matches)

#class TestExtractMarkdownLinks(unittest.TestCase):
    

if __name__ == "__main__":
    unittest.main()