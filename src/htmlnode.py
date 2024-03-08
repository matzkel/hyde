class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # A string representing the value of the HTML tag (e.g. the text inside a paragrapgh)
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props # A dictionary representing the attributes of the HTML tag

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None or not self.props:
            raise ValueError("props dictionary is empty")
        
        props = []
        for key, value in self.props.items():
            props.append(f"{key}=\"{value}\"")
        return " ".join(props)

    def __repr__(self):
        return f"HTMLNode(\n{self.tag},\n{self.value},\n{self.children},\n{self.props}\n)"


class BranchNode(HTMLNode):
    def __init__(self, tag=None, childen=None):
        super().__init__(tag, None, childen, None)

    def to_html(self):
        if self.tag is None or not self.tag:
            raise ValueError("BranchNode requires tag")
        
        if self.children is None or not self.children:
            raise ValueError("BranchNode requires children")

        html_str = f"<{self.tag}>"
        for child in self.children:
            html_str += child.to_html()
        html_str += f"</{self.tag}>"
        return html_str
    
    def __repr__(self):
        return f"BranchNode(\n{self.tag},\n{self.children}\n)"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires value")

        if self.tag is None or not self.tag: # If there is no tag, the value will be rendered as raw text
            return self.value

        try:
            props_str = self.props_to_html()
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        except:
            return f"<{self.tag}>{self.value}</{self.tag}>"
            
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
