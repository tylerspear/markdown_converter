
def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split('\n'):
        if block == '\n':
            continue
        else:
            blocks.append(block.strip())
    return blocks
