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
from Graph import DependencyGraph

JS_LANGUAGE = Language(tsJavaScript.language())

# Initialize the parser
parser = Parser(JS_LANGUAGE)

# Create a graph using NetworkX
graph = DependencyGraph()

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

graph.pretty_print_edges()
graph.pretty_print_nodes()
