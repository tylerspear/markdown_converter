from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
import os
from pathlib import Path

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split('\n\n'):
        if block == "":
            continue
        else:
            blocks.append(block.strip())
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return 'heading'
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)  # Use this instead
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    markdown = markdown.split('\n')

    for line in markdown:
        if line.startswith('#') and line.count('#') == 1:
            return line.split('#')[1].strip() 
    raise Exception("No heading provided in file")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as ffile:
        from_content = ffile.read()
        html_node = markdown_to_html_node(from_content).to_html()
    
    with open(template_path) as tfile:
        template_content = tfile.read()
        title = extract_title(from_content)
        new_content = template_content.replace('{{ Title }}', title)
        new_content = new_content.replace('{{ Content }}', html_node)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path ,'w') as dest:
        dest.write(new_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    try:
        files = os.listdir(dir_path_content)

        with open(template_path) as tfile:
            template_content = tfile.read()

        for file in files:
            full_path = os.path.join(dir_path_content, file)
            if os.path.isfile(full_path) and file.endswith('.md'):
                with open(full_path) as read_file:
                    content = read_file.read()
                    html_node = markdown_to_html_node(content).to_html()
                    title = extract_title(content)
                    
                    new_content = template_content.replace('{{ Title }}', title)
                    new_content = new_content.replace('{{ Content }}', html_node)
                    
                    relative_path = os.path.relpath(full_path, dir_path_content)
                    destination_path = os.path.join(dest_dir_path, os.path.dirname(relative_path))
                    
                    os.makedirs(destination_path, exist_ok=True)
                    with open(os.path.join(destination_path, file.replace('.md', '.html')), 'w') as outfile:                        
                        print(f"Calculated destination path: {destination_path}")
                        outfile.write(new_content)

            elif os.path.isdir(full_path):
                generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, file))

    except FileNotFoundError:
        print(f"Error: Directory '{dir_path_content}' not found.")


        
        
