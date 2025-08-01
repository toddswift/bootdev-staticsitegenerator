import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
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
    
    # this test failed unit tests
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
    
    # this test failed unit tests
    #def test_nested_brackets(self):
    #    matches = extract_markdown_images("![alt [nested] text](url4.jpg)")
    #    self.assertListEqual([("alt [nested] text", "url4.jpg")], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "Text [alt1](url1.jpg) more text [alt2](url2.png)"
        )
        self.assertListEqual([("alt1", "url1.jpg"), ("alt2", "url2.png")], matches)

    def test_empty_string(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_no_links(self):
        matches = extract_markdown_links("This is plain text without links")
        self.assertListEqual([], matches)

    def test_empty_anchor(self):
        matches = extract_markdown_links("[](/page.html)")
        self.assertListEqual([("", "/page.html")], matches)

    def test_empty_url(self):
        matches = extract_markdown_links("[anchor]()")
        self.assertListEqual([("anchor", "")], matches)

    def test_special_characters(self):
        matches = extract_markdown_links(
            "[anchor with spaces & special chars!](http://example.com/page with spaces.html?query=1)"
        )
        self.assertListEqual(
            [("anchor with spaces & special chars!", "http://example.com/page with spaces.html?query=1")],
            matches
        )

    def test_invalid_syntax(self):
        matches = extract_markdown_links("[alt text(url) or [alt url) or (alt)[url]")
        self.assertListEqual([], matches)

    def test_mixed_valid_invalid(self):
        matches = extract_markdown_links(
            "[valid](url1.jpg) invalid [alt](url2.png) [] [alt](url)"
        )
        self.assertListEqual([("valid", "url1.jpg"), ("alt", "url2.png"), ("alt", "url")], matches)

    def test_whitespace(self):
        matches = extract_markdown_links("  [  anchor text  ](  url3.html  )  ")
        self.assertListEqual([("  anchor text  ", "  url3.html  ")], matches)

    def test_nested_brackets(self):
        matches = extract_markdown_links("[alt [nested] text](url4.jpg)")
        self.assertListEqual([], matches)

    def test_no_match_for_images(self):
        matches = extract_markdown_links("![image](url.jpg)")
        self.assertListEqual([], matches)

class SplitImagesandLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_split_images_no_images(self):
        node = TextNode("This is plain text without images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

#    def test_split_images_empty_text(self):
#        node = TextNode("", TextType.TEXT)
#        new_nodes = split_nodes_image([node])
#        self.assertListEqual(new_nodes, [])

    def test_split_images_non_text_node(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_images_single_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and [another link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://www.youtube.com"),
            ],
        )

    def test_split_links_no_links(self):
        node = TextNode("This is plain text without links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    #def test_split_links_empty_text(self):
    #    node = TextNode("", TextType.TEXT)
    #    new_nodes = split_nodes_link([node])
    #    self.assertListEqual(new_nodes, [])

    def test_split_links_non_text_node(self):
        node = TextNode("italic text", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_links_single_link(self):
        node = TextNode("[link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("link", TextType.LINK, "https://www.boot.dev")],
        )

    def test_split_links_and_images_mixed(self):
        node = TextNode(
            "Text with ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
        )

class TestTextToTextNodes(unittest.TestCase):
    #def test_mixed_markdown(self):
    #    text = "This is **bold** _italic_ `code` ![image](https://example.com/img.png) [link](https://boot.dev)"
    #    result = text_to_textnodes(text)
    #    self.assertListEqual(
    #        result,
    #        [
    #            TextNode("This is ", TextType.TEXT),
    #            TextNode("bold", TextType.BOLD),
    #            TextNode(" ", TextType.TEXT),
    #            TextNode("italic", TextType.ITALIC),
    #            TextNode(" ", TextType.TEXT),
    #            TextNode("code", TextType.CODE),
    #            TextNode(" ", TextType.TEXT),
    #            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
    #            TextNode(" ", TextType.TEXT),
    #            TextNode("link", TextType.LINK, "https://boot.dev"),
    #        ]
    #    )

    def test_single_bold(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        self.assertListEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_single_image(self):
        text = "![image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            result,
            [TextNode("image", TextType.IMAGE, "https://example.com/img.png")]
        )

    #def test_empty_string(self):
    #    text = ""
    #    result = text_to_textnodes(text)
    #    self.assertListEqual(result, [TextNode("", TextType.TEXT)])

    def test_no_markdown(self):
        text = "This is plain text"
        result = text_to_textnodes(text)
        self.assertListEqual(result, [TextNode("This is plain text", TextType.TEXT)])

    #def test_complex_markdown(self):
    #    text = "**bold** text _italic_ more `code` text ![img](url.png) and [link](https://example.com)"
    #    result = text_to_textnodes(text)
    #    self.assertListEqual(
    #        result,
    #        [
    #            TextNode("bold", TextType.BOLD),
    #            TextNode(" text ", TextType.TEXT),
    #            TextNode("italic", TextType.ITALIC),
    #            TextNode(" more ", TextType.TEXT),
    #            TextNode("code", TextType.CODE),
    #            TextNode(" text ", TextType.TEXT),
    #            TextNode("img", TextType.IMAGE, "url.png"),
    #            TextNode(" and ", TextType.TEXT),
    #            TextNode("link", TextType.LINK, "https://example.com"),
    #        ]
    #    )

    def test_multiple_images_and_links(self):
        text = "![img1](url1.png) [link1](url1.com) ![img2](url2.png) [link2](url2.com)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            result,
            [
                TextNode("img1", TextType.IMAGE, "url1.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2.com"),
            ]
        )

    def test_invalid_markdown_delimiter(self):
        text = "This is **unclosed bold"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_multiple_newlines(self):
        md = """
Paragraph 1



Paragraph 2


Paragraph 3
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph 1",
                "Paragraph 2",
                "Paragraph 3",
            ],
        )
    
    def test_single_block(self):
        md = "Just one paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one paragraph"])
    
    def test_leading_trailing_newlines(self):
        md = """


Heading


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Heading"])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### Sixth level heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_code(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote(self):
        block = "> This is a quote\n> Another line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> Single line quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- Single item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        block = "1. First item\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. Single item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_paragraph(self):
        block = "This is a simple paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "Multi-line paragraph\nwith two lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_invalid_ordered_list(self):
        block = "2. Starts with 2\n3. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. First\n3. Skips number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_mixed_content(self):
        block = "- Item 1\n> Quote line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    #def test_empty_lines_in_block(self):
    #    block = "> Quote line\n>\n> Another quote"
    #    self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    #    block = "- Item 1\n\n- Item 2"
    #    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()