import json
from pathlib import Path

from code_analysis.python_parser import parse_python_file
from code_analysis.function_extractor import extract_functions
from code_analysis.class_extractor import extract_classes
from code_analysis.import_analyzer import extract_imports
from code_analysis.dependency_analyzer import build_dependency_map


INPUT_FILE = Path(
    "storage/repositories/django_django/file_contents.jsonl"
)

OUTPUT_DIR = Path(
    "storage/analysis/django_django"
)


def analyze_repository():

    file_analysis = []

    with INPUT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            data = json.loads(line)

            if not data["path"].endswith(".py"):
                continue

            tree = parse_python_file(data["content"])

            if tree is None:
                continue

            result = {
                "path": data["path"],
                "sha": data["sha"],
                "functions": extract_functions(tree),
                "classes": extract_classes(tree),
                "imports": extract_imports(tree)
            }

            file_analysis.append(result)

            print(f"Analyzed: {data['path']}")

    dependencies = build_dependency_map(file_analysis)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with (OUTPUT_DIR / "code_analysis.jsonl").open(
        "w",
        encoding="utf-8"
    ) as file:

        for item in file_analysis:
            file.write(
                json.dumps(item) + "\n"
            )

    with (OUTPUT_DIR / "dependencies.json").open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dependencies,
            file,
            indent=4
        )

    print("\nCode analysis completed!")
    print("Analyzed Python files:", len(file_analysis))
    print("Output:", OUTPUT_DIR)


if __name__ == "__main__":
    analyze_repository()