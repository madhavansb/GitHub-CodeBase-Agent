import ast


def parse_python_file(content):

    try:
        return ast.parse(content)

    except SyntaxError:
        return None