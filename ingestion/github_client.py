import os
import requests

from dotenv import load_dotenv

load_dotenv()


class GitHubClient:

    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        })

        token = os.getenv("GITHUB_TOKEN")

        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}"
            })

    def get(self, endpoint, params=None):
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"

        response = self.session.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def get_repository(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}")

    def get_tree(self, owner, repo, tree_sha, recursive=False):
        params = {}

        if recursive:
            params["recursive"] = "1"

        return self.get(
            f"repos/{owner}/{repo}/git/trees/{tree_sha}",
            params=params
        )

    def get_blob(self, owner, repo, sha):
        return self.get(
            f"repos/{owner}/{repo}/git/blobs/{sha}"
        )