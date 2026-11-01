from pyspark.sql import functions as F


def process_files(df):

    processed_df = (
        df
        .withColumn(
            "file_name",
            F.element_at(F.split("path", "/"), -1)
        )
        .withColumn(
            "extension",
            F.lower(
                F.regexp_extract("path", r"\.([^.\/]+)$", 1)
            )
        )
        .withColumn(
            "directory",
            F.regexp_replace("path", r"/[^/]+$", "")
        )
        .withColumn(
            "content_lines",
            F.size(F.split(F.col("content"), "\n"))
        )
        .withColumn(
            "content_characters",
            F.length("content")
        )
    )

    return processed_df