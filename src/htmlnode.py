
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __eq__(self, other):
        if other is None or not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props and
            self.children == other.children
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props}, children={self.children})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        # add a .to_html() method that renders a leaf node as an HTML string
        if not self.value:
            raise ValueError("Leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, props=props, children=children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag.")
        if not self.children:
            raise ValueError("Parent nodes must have children.")
        
        # Get the HTML for all children using recursion
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        # Combine the tag, properties, and children's HTML
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
        
        

        