from textnode import TextNode, TextType
import shutil
import os


def main():
    clean_and_copy('static', 'public')

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