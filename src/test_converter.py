import unittest

from converter import markdown_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headerblock(self):
        md = """
#### This is a header _block_

And a paragraph **block**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>This is a header <i>block</i></h4><p>And a paragraph <b>block</b></p></div>",
        )
        
    def test_quoteblock(self):
        md = """
>This is a quote _block_
>On two lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote <i>block</i>\nOn two lines</blockquote></div>",
        )

    def test_unorderdblock(self):
        md = """- This is an _unordered_ item
- And this is **another** unordered item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an <i>unordered</i> item</li><li>And this is <b>another</b> unordered item</li></ul></div>",
        )


    def test_orderdblock(self):
        md = """1. This is an _ordered_ item
2. And this is **another** ordered item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an <i>ordered</i> item</li><li>And this is <b>another</b> ordered item</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()