import base64

from ingestion.github_client import GitHubClient


MAX_FILE_SIZE = 1_000_000  # 1 MB

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".go", ".rs", ".cpp", ".c",
    ".h", ".cs", ".php", ".rb", ".swift",
    ".kt", ".html", ".css", ".scss",
    ".json", ".yaml", ".yml", ".toml",
    ".md", ".txt", ".xml", ".sql",
    ".sh", ".dockerfile", ".ini"
}

BLOCKED_NAMES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "credentials",
    "secrets.json"
}


def should_fetch_file(path, size):

    if size > MAX_FILE_SIZE:
        return False

    parts = path.lower().split("/")
    filename = parts[-1]

    if filename in BLOCKED_NAMES:
        return False

    if filename.startswith(".env"):
        return False

    if "node_modules" in parts:
        return False

    if ".git" in parts:
        return False

    if "__pycache__" in parts:
        return False

    extension = "." + filename.split(".")[-1] if "." in filename else ""

    return extension in ALLOWED_EXTENSIONS


def extract_file_content(client, owner, repo, file_info):

    result = client.get_blob(
        owner,
        repo,
        file_info["sha"]
    )

    if result.get("encoding") != "base64":
        return None

    raw_content = base64.b64decode(result["content"])

    # Skip binary files.
    if b"\x00" in raw_content:
        return None

    try:
        content = raw_content.decode("utf-8")
    except UnicodeDecodeError:
        return None

    return {
        "path": file_info["path"],
        "sha": file_info["sha"],
        "size": file_info["size"],
        "content": content
    }


def fetch_all_file_contents(repository):

    client = GitHubClient()

    owner = repository["owner"]
    repo = repository["repo"]

    extracted_files = []

    for index, file_info in enumerate(repository["files"], start=1):

        if not should_fetch_file(
            file_info["path"],
            file_info["size"]
        ):
            continue

        try:
            result = extract_file_content(
                client,
                owner,
                repo,
                file_info
            )

            if result:
                extracted_files.append(result)

                print(
                    f"[{index}] Fetched: {file_info['path']}"
                )

        except Exception as error:
            print(
                f"Could not fetch {file_info['path']}: {error}"
            )

    return extracted_files