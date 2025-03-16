import os
from tree_sitter import Language, Parser, Query
import tree_sitter_javascript as tsJavaScript

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f: 
        file_content = f.read()
    ext = os.path.splitext(file_path)[1].lower().lstrip(".")
    return file_content, ext

def print_tree(node, indent=0):
    print("  " * indent + f"{node.type} [{node.start_point} - {node.end_point}]")
    for child in node.children:
        print_tree(child, indent + 1)

if __name__ == "__main__":

    # git.Repo.clone_from(url="https://github.com/sdpa/zoo-management.git", to_path="./src")

    file = "./src/main.js"
    query_file = "./javascript.scm"

    # Parase file using tree-sitter

    # Load the JavaScript grammar
    fileContent, _ = read_file(file)
    query_string, _ = read_file(query_file)

    JS_LANGUAGE = Language(tsJavaScript.language())
    # Initialize the tree-sitter parser
    parser = Parser(JS_LANGUAGE)

    # Parse the JavaScript code
    tree = parser.parse(fileContent.encode())

    query = JS_LANGUAGE.query(query_string)

    captures_dict = query.captures(tree.root_node)

    functions = captures_dict['function']

    for function in functions:
        children = function.children
        text = function.text.decode("utf-8")
        
        print("====================================")
        print(f"{text}")