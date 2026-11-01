import ast


def extract_functions(tree):

    functions = []

    if tree is None:
        return functions

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

            functions.append({
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "parameters": [
                    arg.arg for arg in node.args.args
                ],
                "is_async": isinstance(
                    node,
                    ast.AsyncFunctionDef
                )
            })

    return functions