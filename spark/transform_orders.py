from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_date,
    trim,
    initcap,
    year,
    month,
    dayofmonth,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "orders.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "spark_processed" / "orders"


def create_spark_session():
    """
    Create a local Spark session.
    """
    return (
        SparkSession.builder
        .appName("EcommerceOrderTransformation")
        .master("local[*]")
        .getOrCreate()
    )


def transform_orders_spark(df):
    """
    Clean and transform raw e-commerce orders using PySpark.
    """

    print("Starting PySpark transformation...")

    # Remove duplicate order IDs
    df = df.dropDuplicates(["order_id"])

    # Remove rows with missing critical values
    required_columns = [
        "order_id",
        "customer_id",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "order_date",
        "country",
    ]

    df = df.dropna(subset=required_columns)

    # Convert columns to appropriate data types
    df = (
        df
        .withColumn("order_id", col("order_id").cast("long"))
        .withColumn("quantity", col("quantity").cast("integer"))
        .withColumn("unit_price", col("unit_price").cast("double"))
        .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
    )

    # Remove invalid values
    df = df.filter(
        (col("quantity") > 0)
        & (col("unit_price") > 0)
        & col("order_date").isNotNull()
    )

    # Standardize text columns
    df = (
        df
        .withColumn("customer_id", trim(col("customer_id")))
        .withColumn("product_id", trim(col("product_id")))
        .withColumn("product_name", trim(col("product_name")))
        .withColumn("category", initcap(trim(col("category"))))
        .withColumn("country", initcap(trim(col("country"))))
    )

    # Calculate order amount
    df = df.withColumn(
        "total_amount",
        col("quantity") * col("unit_price")
    )

    # Create date-derived columns
    df = (
        df
        .withColumn("order_year", year(col("order_date")))
        .withColumn("order_month", month(col("order_date")))
        .withColumn("order_day", dayofmonth(col("order_date")))
    )

    print("PySpark transformation completed.")

    return df


def main():
    spark = create_spark_session()

    try:
        print("=" * 60)
        print("PYSPARK E-COMMERCE TRANSFORMATION STARTED")
        print("=" * 60)

        raw_df = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(RAW_DATA_PATH))
        )

        raw_count = raw_df.count()

        print(f"Raw records read by Spark: {raw_count}")

        transformed_df = transform_orders_spark(raw_df)

        clean_count = transformed_df.count()

        print(f"Clean Spark records: {clean_count}")
        print(
            f"Rejected/removed Spark records: "
            f"{raw_count - clean_count}"
        )

        print("\nTransformed Spark schema:")
        transformed_df.printSchema()

        print("\nSample transformed records:")
        transformed_df.orderBy("order_id").show(
            10,
            truncate=False
        )

        (
            transformed_df
            .write
            .mode("overwrite")
            .parquet(str(OUTPUT_PATH))
        )

        print(
            f"Spark output saved to: "
            f"{OUTPUT_PATH}"
        )

        print("=" * 60)
        print("PYSPARK TRANSFORMATION COMPLETED SUCCESSFULLY")
        print("=" * 60)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
