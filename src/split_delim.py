from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #split the string into words
    words = node.text.split()
    nodes = []
    for word in words:
        if word.startswith(f"{delimiter}"):
            new_node = TextNode(word[2:], text_type)
            nodes.append(new_node)
        elif word.endswith(f"{delimiter}"):
            new_node = TextNode(word[:-2], text_type)
            nodes.append(new_node)
        else:
            new_node = TextNode(word, text_type)
            nodes.append(new_node)
    return nodes

            