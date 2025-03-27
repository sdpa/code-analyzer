import networkx as nx
from tree_sitter import Language, Parser
import matplotlib.pyplot as plt
import tree_sitter_javascript as tsJavaScript
from CodeNode import CodeNode
from relations import RelationType
JS_LANGUAGE = Language(tsJavaScript.language())

# Initialize the parser
parser = Parser(JS_LANGUAGE)

# Example JavaScript code (You can replace this with your code input)
javascript_code = """
function foo() {
    console.log("Hello from foo!");
}

const bar = function() {
    foo();
}

const baz = () => {
    bar();
    console.log("Hello from baz!");
}

foo();
"""

# Parse the code
tree = parser.parse(bytes(javascript_code, "utf8"))

# Queries to capture function definitions and calls
function_definition_query = JS_LANGUAGE.query("""
(function_declaration) @function_def
""")

function_call_query = JS_LANGUAGE.query("""
(call_expression) @function_call
""")

# Run the queries to capture function definitions
function_definitions = function_definition_query.captures(tree.root_node)
function_calls = function_call_query.captures(tree.root_node)

# Create a graph using NetworkX
graph = nx.DiGraph()

# Function to extract code blocks from nodes (start and end positions)
def get_code_block(node):
    return javascript_code[node.start_byte:node.end_byte]

functions_detected = {}

# Add nodes for function definitions (with their code blocks)
for match in function_definitions['function_def']:
    function_name = match.child_by_field_name('name').text.decode('utf-8')
    code_node = CodeNode(type_="function_definition", file_path="test.js", tree_node=match)

    functions_detected[function_name] = code_node.node_id

    graph.add_node(code_node.node_id, node_object=code_node)

# Add edges for function calls (with the caller and callee function names)
for match in function_calls['function_call']:
    function_called = match.child_by_field_name('function').text.decode('utf-8')
    code_node = CodeNode(type_="function_call", file_path="test.js", tree_node=match)

    graph.add_node(code_node.node_id, node_object=code_node)

    if function_called in functions_detected:
        target_node_id = functions_detected.get(function_called)

        graph.add_edge(code_node.node_id, target_node_id, label=RelationType.CALLS)
        graph.add_edge(target_node_id, code_node.node_id, label = RelationType.CALLED_BY)



print("\nGraph information")
for edge in graph.edges(data=True):

    source_node = graph.nodes.get(edge[0])
    target_node = graph.nodes.get(edge[1])

    print(f"{source_node['node_object'].code_block} -- {edge[2]['label'].name} --> {target_node['node_object'].code_block}")