import json

from pathlib import Path

from ingestion.repo_fetch import fetch_repository
from ingestion.file_extract import fetch_all_file_contents
from ingestion.tree_build import build_file_tree


def save_json(data, filepath):

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    repository_url = input(
        "Enter GitHub repository URL: "
    ).strip()

    # Step 1: Fetch repository structure.
    repository = fetch_repository(repository_url)

    print("\nRepository structure fetched!")
    print("Total files:", len(repository["files"]))
    print("Total folders:", len(repository["folders"]))

    # Step 2: Build nested folder structure.
    folder_tree = build_file_tree(
        repository["files"],
        repository["folders"]
    )

    # Step 3: Fetch file contents.
    print("\nFetching file contents...")

    extracted_files = fetch_all_file_contents(repository)

    # Step 4: Prepare output directory.
    output_dir = (
        Path("storage")
        / "repositories"
        / f"{repository['owner']}_{repository['repo']}"
    )

    # Step 5: Save repository metadata.
    save_json(
        {
            key: value
            for key, value in repository.items()
            if key not in ("files", "folders")
        },
        output_dir / "metadata.json"
    )

    # Step 6: Save nested folder tree.
    save_json(
        folder_tree,
        output_dir / "folder_tree.json"
    )

    # Step 7: Save file information and contents.
    with open(
        output_dir / "file_contents.jsonl",
        "w",
        encoding="utf-8"
    ) as file:

        for item in extracted_files:
            file.write(
                json.dumps(item, ensure_ascii=False) + "\n"
            )

    print("\nRepository fetching completed!")
    print("Fetched text files:", len(extracted_files))
    print("Saved to:", output_dir)


if __name__ == "__main__":
    main()