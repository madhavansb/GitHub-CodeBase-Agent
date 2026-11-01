import json
from pathlib import Path


INPUT_FILE = Path(
    "storage/repositories/django_django/file_contents.jsonl"
)

ANALYSIS_FILE = Path(
    "storage/analysis/django_django/code_analysis.jsonl"
)


def load_analysis():

    analysis = {}

    with ANALYSIS_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)
            analysis[item["path"]] = item

    return analysis


def create_code_chunks():

    analysis = load_analysis()
    chunks = []

    with INPUT_FILE.open("r", encoding="utf-8") as file:

        for line in file:

            data = json.loads(line)
            path = data["path"]

            if not path.endswith(".py"):
                continue

            metadata = analysis.get(path)

            if not metadata:
                continue

            source_lines = data["content"].splitlines()

            symbols = (
                metadata["classes"] + metadata["functions"]
            )

            for symbol in symbols:

                start = symbol["start_line"]
                end = symbol["end_line"]

                code = "\n".join(
                    source_lines[start - 1:end]
                )

                chunks.append({
                    "file_path": path,
                    "symbol_name": symbol["name"],
                    "start_line": start,
                    "end_line": end,
                    "code": code
                })

    return chunks


if __name__ == "__main__":

    chunks = create_code_chunks()

    print("Total code chunks:", len(chunks))

    for chunk in chunks[:3]:
        print("\n", chunk["file_path"])
        print(chunk["symbol_name"])
        print(chunk["code"][:300])