from textnode import TextNode, TextType
import re

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