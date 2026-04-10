import re
from enum import Enum
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    final_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if len(block) != 0: final_blocks.append(block.strip(" \n"))
    return final_blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block) != None: return BlockType.HEADING
    elif re.fullmatch(r"^`{3}\n[\w\s\d\*\\\.]*`{3}$", block) != None: return BlockType.CODE
    elif re.fullmatch(r"^(>.*\n?)*", block) != None: return BlockType.QUOTE
    elif re.fullmatch(r"^(- .*\n?)*", block) != None: return BlockType.UNORDERED_LIST
    elif re.fullmatch(r"^(\d\. .*\n?)*", block) != None:
        matches = re.findall(r"^\d\. ", block, flags=re.MULTILINE)
        ctr = 1
        good = True
        for match in matches:
            if int(match[0]) == ctr: ctr += 1
            else: 
                good = False
                break
        if good: return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH