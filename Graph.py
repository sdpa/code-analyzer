import networkx as nx
from rich.console import Console
from rich.table import Table
from rich.text import Text

class DependencyGraph(nx.DiGraph):

    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

    def pretty_print_edges(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_column("Code Segment 1", style="cyan", no_wrap=False)
        table.add_column("Relation", style="yellow", justify="center")
        table.add_column("Code Segment 2", style="green", no_wrap=False)

        for edge in self.edges(data=True):
            source_node = self.nodes.get(edge[0])
            target_node = self.nodes.get(edge[1])

            # print(f"{source_node['node_object'].code_block} -- {edge[2]['label'].name} --> {target_node['node_object'].code_block}")

            code_left = source_node['node_object'].code_block
            code_right = target_node['node_object'].code_block
            file_left = source_node['node_object'].file_path
            file_right = target_node['node_object'].file_path
            relation = edge[2]['label'].name

            left_column = Text(code_left, style="cyan")
            left_column.append(f"\n\n[{file_left}]", style="red")

            # Format right column: code + file name in red
            right_column = Text(code_right, style="green")
            right_column.append(f"\n\n[{file_right}]", style="red")
            
            table.add_row(left_column, relation, right_column)

        console.print(table)

    def pretty_print_nodes(self):
        console = Console()
        table = Table(show_header=False, show_lines=True)
        table.add_column("Code Segment 1", style="cyan", no_wrap=False)

        for node in self.nodes(data=True):
            file_path = node[0]
            content = node[1]['node_object'].code_block

            content = Text(content, style="cyan")
            content.append(f"\n\n[{file_path}]", style="red")
            
            table.add_row(content)
        
        console.print(table)