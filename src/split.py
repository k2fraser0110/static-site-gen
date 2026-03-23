import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: final_nodes.append(node)
        else:
            new_nodes = []
            old_split = node.text.split(delimiter)
            if len(old_split) % 2 == 1:
                for i in range(0, len(old_split)):
                    if i % 2 == 0: new_nodes.append(TextNode(old_split[i], TextType.TEXT))
                    else: new_nodes.append(TextNode(old_split[i], text_type))
                final_nodes.extend(new_nodes)   
            else:
                raise Exception(f"Invalid markdown in TextNode({node.text},{node.text_type})")
    return final_nodes

def split_nodes_image(old_nodes):
    final_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: final_nodes.append(node)
        else:
            new_nodes = []
            matches = extract_markdown_images(node.text)
            curr_index = 0
            for match in matches:
                find_index = node.text.find(match[0], curr_index)
                new_nodes.append(TextNode(node.text[curr_index:find_index-2], TextType.TEXT))
                new_nodes.append(TextNode(match[0],TextType.IMAGE,match[1]))
                curr_index = (find_index + len(match[0]) + len(match[1]) + 3)
            if curr_index < len(node.text) : new_nodes.append(TextNode(node.text[curr_index:], TextType.TEXT))
            final_nodes.extend(new_nodes)
    return final_nodes

def split_nodes_link(old_nodes):
    final_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: final_nodes.append(node)
        else:
            new_nodes = []
            matches = extract_markdown_links(node.text)
            curr_index = 0
            for match in matches:
                find_index = node.text.find(match[0], curr_index)
                new_nodes.append(TextNode(node.text[curr_index:find_index-1], TextType.TEXT))
                new_nodes.append(TextNode(match[0],TextType.LINK,match[1]))
                curr_index = (find_index + len(match[0]) + len(match[1]) + 3)
            if curr_index < len(node.text): new_nodes.append(TextNode(node.text[curr_index:], TextType.TEXT))
            final_nodes.extend(new_nodes)
    return final_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

