from textnode import TextNode, TextType
import re
from enum import Enum

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
        # Pattern matches ![alt text](url)
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        # Find all matches and return list of tuples with alt text and URL
        return re.findall(pattern, text)

def extract_markdown_links(text):
    # Pattern matches [anchor text](url)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # Find all matches and return list of tuples with anchor text and URL
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        # Process the first image only
        alt_text, url = images[0]
        delimiter = f"![{alt_text}]({url})"
        sections = old_node.text.split(delimiter, 1)
        # Handle before text
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        # Add the image node
        new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        # Recursively process the remaining text
        if len(sections) > 1 and sections[1]:
            remaining_nodes = split_nodes_image([TextNode(sections[1], TextType.TEXT)])
            new_nodes.extend(remaining_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        # Process the first link only
        anchor_text, url = links[0]
        delimiter = f"[{anchor_text}]({url})"
        sections = old_node.text.split(delimiter, 1)
        # Handle before text
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        # Add the link node
        new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
        # Recursively process the remaining text
        if len(sections) > 1 and sections[1]:
            remaining_nodes = split_nodes_link([TextNode(sections[1], TextType.TEXT)])
            new_nodes.extend(remaining_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    # Split the markdown string by double newlines
    blocks = markdown.split("\n\n")
    # Process each block
    processed_blocks = []
    for block in blocks:
        # Strip whitespace and skip empty blocks
        stripped_block = block.strip()
        if stripped_block:
            processed_blocks.append(stripped_block)
    return processed_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # Check for heading (1-6 # followed by space)
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with triple backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines if line.strip()):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith("- ") for line in lines if line.strip()):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with number, period, space, starting at 1)
    if lines and all(line.strip() for line in lines):
        ol_pattern = r"^\d+\.\s"
        if all(re.match(ol_pattern, line) for line in lines):
            # Verify numbers start at 1 and increment
            numbers = [int(re.match(r"(\d+)", line).group(1)) for line in lines]
            if numbers == list(range(1, len(numbers) + 1)):
                return BlockType.ORDERED_LIST
    
    # Default to paragraph if no other type matches
    return BlockType.PARAGRAPH