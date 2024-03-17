import unittest

from blocks import (
    BlockType,

    block_to_block_type,
    markdown_to_blocks
)

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items"""
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here",
                "This is the same paragraph on a new line",
                "* This is a list",
                "* with items"
            ], markdown_to_blocks(markdown)
        )

    def test_markdown_to_blocks2(self):
        markdown = """This is normal paragraph
        This is another paragraph, but it includes **bold** and *italic* text
        
        * This is a list
        * with item 1
        * and item 2"""
        self.assertEqual(
            [
                "This is normal paragraph",
                "This is another paragraph, but it includes **bold** and *italic* text",
                "* This is a list",
                "* with item 1",
                "* and item 2"
            ], markdown_to_blocks(markdown)
        )
    
    def test_block_to_block_type(self):
        block = "1. This is an ordered list"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_block_to_block_type2(self):
        block = "```This is not a code block!"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_block_type3(self):
        block = "###This is huge heading!"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_block_type4(self):
        block = ""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))


if __name__ == "__main__":
    unittest.main()
