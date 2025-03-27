import networkx as nx
from tree_sitter import Language, Parser
import matplotlib.pyplot as plt
import tree_sitter_javascript as tsJavaScript
from CodeNode import CodeNode
from relations import RelationType
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text

JS_LANGUAGE = Language(tsJavaScript.language())

# Initialize the parser
parser = Parser(JS_LANGUAGE)

# Create a graph using NetworkX
graph = nx.DiGraph()

def get_source_files(directory, extension):
    js_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                js_files.append(os.path.join(root, file))
    return js_files

def analyze_invocation_relations(src: str, graph: nx.DiGraph):

    # Queries to capture function definitions and calls
    function_definition_query = JS_LANGUAGE.query("""
    (function_declaration) @function_def

    (lexical_declaration
        (variable_declarator
        name: (identifier) @name
        value: [(arrow_function) (function_expression)]) @function_def)
                                                  
    (variable_declaration
        (variable_declarator
        name: (identifier) @name
        value: [(arrow_function) (function_expression)]) @function_df)
    """)

    function_call_query = JS_LANGUAGE.query("""
    (call_expression) @function_call
    """)

    files = get_source_files("./src", ".js")
   

    for file in files:
        # Run the queries to capture function definitions
        with open(file, "r", encoding="utf-8") as file:
            source_code = file.read()
            tree = parser.parse(bytes(source_code, "utf8"))
            function_definitions = function_definition_query.captures(tree.root_node)
            function_calls = function_call_query.captures(tree.root_node)
            functions_detected = {}
            # Add nodes for function definitions (with their code blocks)
            if 'function_def' in function_definitions:
                for match in function_definitions['function_def']:
                    function_name = match.child_by_field_name('name').text.decode('utf-8')
                    code_node = CodeNode(type_="function_definition", file_path=file.name, tree_node=match)

                    functions_detected[function_name] = code_node.node_id

                    graph.add_node(code_node.node_id, node_object=code_node)

            # Add edges for function calls (with the caller and callee function names)
            if 'function_call' in function_calls:
                for match in function_calls['function_call']:
                    function_called = match.child_by_field_name('function').text.decode('utf-8')
                    code_node = CodeNode(type_="function_call", file_path=file.name, tree_node=match)

                    graph.add_node(code_node.node_id, node_object=code_node)

                    if function_called in functions_detected:
                        target_node_id = functions_detected.get(function_called)

                        graph.add_edge(code_node.node_id, target_node_id, label=RelationType.CALLS)
                        graph.add_edge(target_node_id, code_node.node_id, label = RelationType.CALLED_BY)

analyze_invocation_relations("./src", graph)

def pretty_print(code_left, file_left, code_right, file_right, relation, table, console):

    
    
    # Format left column: code + file name in red
    left_column = Text(code_left, style="cyan")
    left_column.append(f"\n\n[{file_left}]", style="red")

    # Format right column: code + file name in red
    right_column = Text(code_right, style="green")
    right_column.append(f"\n\n[{file_right}]", style="red")
    
    table.add_row(left_column, relation, right_column)


console = Console()
table = Table(show_header=False, show_lines=True)
table.add_column("Code Segment 1", style="cyan", no_wrap=False)
table.add_column("Relation", style="yellow", justify="center")
table.add_column("Code Segment 2", style="green", no_wrap=False)

for edge in graph.edges(data=True):

    source_node = graph.nodes.get(edge[0])
    target_node = graph.nodes.get(edge[1])

    # print(f"{source_node['node_object'].code_block} -- {edge[2]['label'].name} --> {target_node['node_object'].code_block}")

    code_left = source_node['node_object'].code_block
    code_right = target_node['node_object'].code_block
    file_left = source_node['node_object'].file_path
    file_right = target_node['node_object'].file_path
    relation = edge[2]['label'].name

    pretty_print(code_left, file_left, code_right, file_right, relation, table, console), 

    # print("="*40)
   
console.print(table)


