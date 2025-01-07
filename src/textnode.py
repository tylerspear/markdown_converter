from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self, text, type, url=None):
        self.text = text
        self.text_type = type
        self.url = url
    
    def __eq__(self, other):
        return (self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("Text type not valid")
    
        if TextType.NORMAL:
            return LeafNode(None, text_node.text)
        if TextType.BOLD:
            return LeafNode("b", text_node.text)
        if TextType.ITALIC:
            return LeafNode("i", text_node.text)
        if TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        if TextType.IMAGE:
            return LeafNode("img", None, {"src":text_node.url, "alt":text_node.text})
        if TextType.CODE:
            return LeafNode("code", text_node.text)



        




