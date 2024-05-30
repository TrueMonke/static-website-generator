class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            if (
                (self.tag == other.tag)
                and (self.value == other.value)
                and (self.children == other.children)
                and (self.props == other.props)
            ):
                return True
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def props_to_html(self):

        props_html_str = ""

        if self.props:

            for key, value in self.props.items():
                props_html_str += f' {key}="{value}"'

        return props_html_str

    def to_html(self):

        raise NotImplementedError
