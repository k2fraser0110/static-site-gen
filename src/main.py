from textnode import TextNode
from textnode import TextType

def main():
    textnode = TextNode("hello", TextType.BOLD, "url")
    print(textnode)

if __name__ == "__main__":
    main()

