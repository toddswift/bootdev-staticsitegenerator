from src.htmlnode import LeafNode
from src.textnode import TextType

def text_node_to_html_node(text_node):
    # It should handle each type of the TextType enum. 
    # If it gets a TextNode that is none of those types, 
    # it should raise an exception. Otherwise, 
    # it should return a new LeafNode object.
    # TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
    # TextType.BOLD: This should return a LeafNode with a "b" tag and the text
    # TextType.ITALIC: "i" tag, text
    # TextType.CODE: "code" tag, text
    # TextType.LINK: "a" tag, anchor text, and "href" prop
    # TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text, props=None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text, props=None)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text, props=None)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text, props=None)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")