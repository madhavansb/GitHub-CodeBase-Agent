from urllib.parse import urlparse

from ingestion.github_client import GitHubClient


def parse_repository_url(url):

    parsed = urlparse(url.strip())

    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
    ):
        raise ValueError("Please provide a valid HTTPS GitHub URL.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) != 2 or not all(parts):
        raise ValueError("URL must look like https://github.com/owner/repo")

    owner, repo = parts

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


def fetch_complete_tree(client, owner, repo, root_sha):

    # First, try fetching the entire tree recursively.
    result = client.get_tree(
        owner,
        repo,
        root_sha,
        recursive=True
    )

    if not result.get("truncated", False):
        return result["tree"]

    print("Large repository detected. Fetching folders individually...")

    all_items = []
    pending_trees = [(root_sha, "")]

    while pending_trees:

        tree_sha, parent_path = pending_trees.pop()

        result = client.get_tree(
            owner,
            repo,
            tree_sha,
            recursive=False
        )

        if result.get("truncated", False):
            raise RuntimeError(
                f"Subtree response was truncated: {parent_path}"
            )

        for item in result["tree"]:

            full_path = (
                f"{parent_path}/{item['path']}"
                if parent_path
                else item["path"]
            )

            item["path"] = full_path
            all_items.append(item)

            if item["type"] == "tree":
                pending_trees.append(
                    (item["sha"], full_path)
                )

    return all_items


def fetch_repository(url):

    client = GitHubClient()

    owner, repo = parse_repository_url(url)

    print(f"Fetching repository: {owner}/{repo}")

    metadata = client.get_repository(owner, repo)

    branch = metadata["default_branch"]

    branch_info = client.get(
        f"repos/{owner}/{repo}/branches/{branch}"
    )

    root_sha = branch_info["commit"]["commit"]["tree"]["sha"]

    tree = fetch_complete_tree(
        client,
        owner,
        repo,
        root_sha
    )

    files = []
    folders = []

    for item in tree:

        if item["type"] == "tree":
            folders.append(item["path"])

        elif item["type"] == "blob":
            files.append({
                "path": item["path"],
                "sha": item["sha"],
                "size": item.get("size", 0)
            })

    return {
        "owner": owner,
        "repo": repo,
        "branch": branch,
        "commit_sha": branch_info["commit"]["sha"],
        "repository_url": url,
        "files": files,
        "folders": folders
    }