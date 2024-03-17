from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("*") or block.startswith("-"):
        return BlockType.UNORDERED_LIST
    elif block[:1].isdigit() and block[1:2].startswith("."):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split("\n"):
        result_line = line.strip()
        if result_line != "":
            blocks.append(result_line)
    return blocks
