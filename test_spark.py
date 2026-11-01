from spark_processing.spark_session import create_spark_session

spark = create_spark_session()

data = [
    ("main.py", "Python"),
    ("app.js", "JavaScript"),
    ("index.html", "HTML"),
]

df = spark.createDataFrame(
    data,
    ["file_name", "language"]
)

df.show()

spark.stop()