from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag:str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, children = None, props=props)
    
    def __eq__(self, other):
        if isinstance(other, LeafNode):
            if (self.tag == other.tag) \
            and (self.value == other.value) \
            and (self.props == other.props):
                return True
        return False


    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


    def to_html(self):
        if self.value:
            if not self.tag:
                return f"{self.value}" 
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" 
        else:
            if self.value == "":
                print("LeafNode")
                print(self)
            raise ValueError(f"LeafNode has no value: {self}")
