from collections import defaultdict


def build_dependency_map(file_analysis):

    dependency_map = defaultdict(list)

    for file_data in file_analysis:

        file_path = file_data["path"]

        for imported in file_data["imports"]:

            dependency_map[file_path].append(
                imported["module"]
            )

    return dict(dependency_map)