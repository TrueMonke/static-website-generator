from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag:str, children: list, props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def children_to_html(self):

        html_children = ""

        for child in self.children:
            if child.tag == "p" and self.tag == "p":
                raise ValueError("Invalid Nesting, can't nest <p> tags")
            html_children+=child.to_html()

        return html_children


    def to_html(self):
        if self.tag:
            if self.children:
                return f"<{self.tag}{self.props_to_html()}>{self.children_to_html()}</{self.tag}>" 
            else:
                raise ValueError("ParentNode has no children")
        else:
            raise ValueError("ParentNode has no tag")
