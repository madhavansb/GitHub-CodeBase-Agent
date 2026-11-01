import json
from pathlib import Path


class RepositoryLookup:

    def __init__(self, repo_path="storage/repositories/django_django"):

        self.repo_path = Path(repo_path)

        with open(self.repo_path / "file_contents.jsonl") as f:
            self.files = [
                json.loads(line)
                for line in f
                if line.strip()
            ]

    def get_file(self, file_path):

        for file in self.files:

            if file.get("path") == file_path:
                return file

        return None

    def search_file(self, filename):

        return [
            file for file in self.files
            if file.get("path", "").endswith(filename)
        ]