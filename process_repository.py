from pathlib import Path

from spark_processing.spark_session import create_spark_session
from spark_processing.data_loader import load_repository_data
from spark_processing.file_processor import process_files
from spark_processing.language_classifier import classify_languages

from spark_processing.repository_statistics import (
    get_language_statistics,
    get_directory_statistics,
    get_largest_files
)


def main():

    repository_name = "django_django"

    input_path = (
        f"storage/repositories/{repository_name}/file_contents.jsonl"
    )

    output_path = (
        f"storage/processed/{repository_name}"
    )

    spark = create_spark_session()

    try:

        # 1. Load repository data.
        print("\nLoading repository data...")

        df = load_repository_data(spark, input_path)

        print("\nOriginal schema:")
        df.printSchema()

        # 2. Process file metadata.
        print("\nProcessing files...")

        processed_df = process_files(df)

        # 3. Classify programming languages.
        print("\nClassifying languages...")

        processed_df = classify_languages(processed_df)

        # 4. Display processed data.
        print("\nProcessed repository files:")

        processed_df.select(
            "path",
            "extension",
            "language",
            "size",
            "content_lines"
        ).show(20, truncate=False)

        # 5. Language statistics.
        print("\nLanguage statistics:")

        get_language_statistics(
            processed_df
        ).show(truncate=False)

        # 6. Directory statistics.
        print("\nDirectory statistics:")

        get_directory_statistics(
            processed_df
        ).show(20, truncate=False)

        # 7. Largest files.
        print("\nLargest files:")

        get_largest_files(
            processed_df
        ).show(truncate=False)

        # 8. Save processed dataset.
        print("\nSaving Parquet dataset...")

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        processed_df.write.mode("overwrite").parquet(
            output_path
        )

        print("\nProcessing completed!")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()