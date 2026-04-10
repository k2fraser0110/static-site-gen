from block import markdown_to_blocks, block_to_block_type, BlockType
from split import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_children(block.strip()))
    return ParentNode("div", children)

def block_to_children(block):
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block.replace("\n", " ")))
        case BlockType.CODE:
            clean_block = block.strip()
            clean_block = clean_block[4:len(clean_block)-3]
            return ParentNode("pre", [LeafNode("code", clean_block)])
        case BlockType.HEADING:
            header_num = 0
            while block[header_num] == "#": header_num += 1
            return ParentNode(f"h{header_num}", text_to_children(block[header_num+1:]))
        case BlockType.QUOTE:
            clean_quote = "\n".join([x[1:] for x in block.split("\n")])
            return ParentNode("blockquote", text_to_children(clean_quote))
        case BlockType.UNORDERED_LIST:
            clean_list = [x[2:] for x in block.split("\n")]
            children = []
            for item in clean_list:
                children.append(ParentNode("li", text_to_children(item)))
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            clean_list = [x[3:] for x in block.split("\n")]
            children = []
            for item in clean_list:
                children.append(ParentNode("li", text_to_children(item)))
            return ParentNode("ol", children)

def text_to_children(text):
    children = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children
