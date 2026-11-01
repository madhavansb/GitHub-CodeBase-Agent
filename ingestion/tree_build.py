def build_file_tree(files, folders):

    root = {}

    # Add folders first.
    for folder in folders:

        parts = folder.split("/")
        current = root

        for part in parts:
            current = current.setdefault(part, {})

    # Add files.
    for file in files:

        parts = file["path"].split("/")
        current = root

        for part in parts[:-1]:
            current = current.setdefault(part, {})

        current[parts[-1]] = {
            "type": "file",
            "sha": file["sha"],
            "size": file["size"]
        }

    return root