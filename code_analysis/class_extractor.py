import ast


def extract_classes(tree):

    classes = []

    if tree is None:
        return classes

    for node in ast.walk(tree):

        if isinstance(node, ast.ClassDef):

            methods = []

            for child in node.body:

                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):

                    methods.append({
                        "name": child.name,
                        "start_line": child.lineno,
                        "end_line": child.end_lineno
                    })

            classes.append({
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "methods": methods
            })

    return classes