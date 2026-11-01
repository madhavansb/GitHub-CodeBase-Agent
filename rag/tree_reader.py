import json
from pathlib import Path


class RepositoryTreeReader:

    def __init__(self, repo_path="storage/repositories/django_django"):

        self.tree_path = Path(repo_path) / "folder_tree.json"

    def get_tree(self):

        with open(self.tree_path) as f:
            return json.load(f)