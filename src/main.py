from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from converter import markdown_to_html_node
import os
import shutil
import sys

def main():
    basepath = "/"
    if sys.argv[0] != "":
        basepath = sys.argv[0]
    directory_copy("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def directory_copy(src, dest):
    source_path = f"{os.getcwd()}/{src}/"
    dest_path = f"{os.getcwd()}/{dest}/"

    if not os.path.exists(source_path): return
    if not os.path.exists(dest_path): os.mkdir(dest_path)

    for file_name in os.listdir(source_path):
        full_path = f"{source_path}/{file_name}"
        if os.path.isfile(full_path):
            shutil.copy(full_path, dest_path)
        else:
            directory_copy(f"{src}/{file_name}", f"{dest}/{file_name}")

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line[:2] == "# ": return line[2:]
    raise Exception("No header line")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(dir_path_content, dest_dir_path)
    full_dir_path = f"{os.getcwd()}/{dir_path_content}/"
    full_dest_path = f"{os.getcwd()}/{dest_dir_path}/"
    full_temp_path = f"{os.getcwd()}/{template_path}"

    for file_name in os.listdir(full_dir_path):
        if os.path.isfile(full_dir_path + file_name) and file_name[-3:] == ".md":
            with open(full_dir_path + file_name, "r") as f:
                markdown = f.read()
            f.close()

            node = markdown_to_html_node(markdown)
            html = node.to_html()
            title = extract_title(markdown)

            with open(full_temp_path, "r") as f:
                template = f.read()
            f.close()

            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            template = template.replace('href="/', f'href="{basepath}')
            template = template.replace('src="/', f'src="{basepath}')

            with open(full_dest_path + file_name[:len(file_name)-3] + ".html", "w") as f:
                f.write(template)
            f.close()
        elif not os.path.isfile(full_dir_path + file_name):
            if not os.path.exists(full_dest_path + file_name): os.mkdir(full_dest_path + file_name)
            generate_pages_recursive(f"{dir_path_content}/{file_name}", template_path, f"{dest_dir_path}/{file_name}", basepath)

def generate_page(from_path, template_path, dest_path):
    full_from_path = f"{os.getcwd()}/{from_path}"
    full_dest_path = f"{os.getcwd()}/{dest_path}"
    full_temp_path = f"{os.getcwd()}/{template_path}"
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(full_from_path, "r") as f:
        markdown = f.read()
    f.close()

    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)

    with open(full_temp_path, "r") as f:
        template = f.read()
    f.close()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)


    with open(full_dest_path, "w") as f:
        f.write(template)
    f.close



    



if __name__ == "__main__":
    main()

