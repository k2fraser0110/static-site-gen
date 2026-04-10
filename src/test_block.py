import unittest
from block import markdown_to_blocks, block_to_block_type, BlockType

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_paragraph_block_good_1(self):
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_paragraph_block_good_2(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_paragraph_block_bad_1(self):
        block = "###This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_block_bad_2(self):
        block = "####### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_good(self):
        block = """```
Here is some code
Here is some more code 
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_bad(self):
        block = """```
Here is some code
Here is some more code
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_good(self):
        block = """> some quotes
> more quotesHere is some code
>and some more"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_bad(self):
        block = """>here are some quotes
Not a quote line
> a quote line
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_block_good(self):
        block = """- line item
- line item 2
- line item 3"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_block_bad(self):
        block = """- line items

- another line
- a quote line
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_block_good(self):
        block = """1. line item
2. line item 2
3. line item 3"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_unordered_block_bad(self):
        block = """1. line item
3. line item 2
4. line item 3"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()