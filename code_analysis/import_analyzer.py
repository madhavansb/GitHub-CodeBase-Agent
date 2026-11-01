import ast


def extract_imports(tree):

    imports = []

    if tree is None:
        return imports

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                imports.append({
                    "module": alias.name,
                    "type": "import"
                })

        elif isinstance(node, ast.ImportFrom):

            imports.append({
                "module": node.module,
                "type": "from_import",
                "level": node.level,
                "names": [
                    alias.name for alias in node.names
                ]
            })

    return imports