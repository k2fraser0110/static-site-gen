class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child classes must override this method")

    def props_to_html(self):
        result = ""
        if len(self.props) == 0 or self.props == None: return result
        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None: raise ValueError("LeafNode.Value must have a value")
        if self.tag == None: return self.value

        result = f"<{self.tag}"
        if self.props != None: result += self.props_to_html()
        result += f">{self.value}</{self.tag}>"

        return result
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None: raise ValueError("ParentNode must have a tag")
        if self.children == None: raise ValueError("ParentNode must have children")

        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"

        return result
    

