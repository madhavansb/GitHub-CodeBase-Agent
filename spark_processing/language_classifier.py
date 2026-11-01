from pyspark.sql import functions as F


def classify_languages(df):

    language_map = {
        "py": "Python",
        "js": "JavaScript",
        "jsx": "React",
        "ts": "TypeScript",
        "tsx": "React TypeScript",
        "java": "Java",
        "go": "Go",
        "rs": "Rust",
        "cpp": "C++",
        "c": "C",
        "html": "HTML",
        "css": "CSS",
        "scss": "SCSS",
        "json": "JSON",
        "yaml": "YAML",
        "yml": "YAML",
        "md": "Markdown",
        "sql": "SQL",
        "xml": "XML",
        "sh": "Shell",
        "toml": "TOML",
        "php": "PHP",
        "rb": "Ruby"
    }

    mapping_expression = F.create_map(
        *[
            item
            for key, value in language_map.items()
            for item in (F.lit(key), F.lit(value))
        ]
    )

    return df.withColumn(
        "language",
        F.coalesce(
            F.element_at(mapping_expression, F.col("extension")),
            F.lit("Other")
        )
    )