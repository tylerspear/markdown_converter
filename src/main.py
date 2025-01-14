from textnode import TextNode, TextType
from block_markdown import generate_page, generate_pages_recursive
import shutil
import os


def main():
    clear_public()
    clean_and_copy('static', 'public')
    generate_pages_recursive(
        "content",        # from_path (your markdown file)
        "template.html",           # template_path (your HTML template)
        "public"        # dest_path (where to save the final HTML)
    )

def clear_public():
    if os.path.exists('public'):
        shutil.rmtree('public')
    os.makedirs('public')

def clean_and_copy(source_dir, dest_dir):
    # Ensure destination directory exists, if not, create it
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Delete all contents in the destination directory
    for item in os.listdir(dest_dir):
        item_path = os.path.join(dest_dir, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

    # Recursively copy all contents from source_dir to dest_dir
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)

        if os.path.isdir(source_item):
            # Recursively copy directories
            shutil.copytree(source_item, dest_item)
        else:
            # Copy files
            shutil.copy2(source_item, dest_item)

if __name__ == "__main__":
    main()