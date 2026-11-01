from pyspark.sql import functions as F


def get_language_statistics(df):

    return (
        df.groupBy("language")
        .agg(
            F.count("*").alias("total_files"),
            F.sum("size").alias("total_size_bytes"),
            F.sum("content_lines").alias("total_lines")
        )
        .orderBy(F.desc("total_files"))
    )


def get_directory_statistics(df):

    return (
        df.groupBy("directory")
        .agg(
            F.count("*").alias("total_files"),
            F.sum("size").alias("total_size_bytes")
        )
        .orderBy(F.desc("total_files"))
    )


def get_largest_files(df):

    return (
        df.select("path", "size", "language")
        .orderBy(F.desc("size"))
        .limit(10)
    )