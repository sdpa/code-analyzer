# Define the custom object for nodes
from tree_sitter import Node
import os

class CodeNode:
    def __init__(self, type_: str, file_path: str, tree_node: Node):
        self.type = type_
        self.code_block = tree_node.text.decode('utf-8')
        self.tree_node = tree_node
        self.file_path = file_path
        self.node_id = self.generate_node_id()

    def __repr__(self):
        return f"CodeNode(type={self.type}, label={self.label})"
    
    def generate_node_id(self):

        normalized_path = os.path.normpath(self.file_path)

        unique_id = f"{normalized_path}:R{self.tree_node.start_point.row}C{self.tree_node.start_point.column}-R{self.tree_node.end_point.row}C{self.tree_node.end_point.column}"

        return unique_id