from pyspark.sql import DataFrame, SparkSession


def load_repository_data(
    spark: SparkSession,
    file_path: str
) -> DataFrame:

    df = (
        spark.read
        .option("multiLine", "false")
        .json(file_path)
    )

    return df