from extract import extract_orders
from data_quality import run_data_quality_checks
from transform import transform_orders, save_transformed_data
from load import load_to_postgres


def run_pipeline():
    """
    Run the complete e-commerce ETL pipeline.

    Steps:
    1. Extract raw order data
    2. Run data-quality checks
    3. Clean and transform data
    4. Save processed data
    5. Load transformed data into PostgreSQL
    """

    print("=" * 50)
    print("E-COMMERCE ETL PIPELINE STARTED")
    print("=" * 50)

    print("\n[1/4] Extracting raw data...")
    raw_df = extract_orders()

    print("\n[2/4] Validating raw data...")
    run_data_quality_checks(raw_df)

    print("[3/4] Transforming data...")
    transformed_df = transform_orders(raw_df)

    save_transformed_data(transformed_df)

    print("\n[4/4] Loading data into PostgreSQL...")
    load_to_postgres(transformed_df)

    print("\n" + "=" * 50)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 50)

    print(f"Raw records: {len(raw_df)}")
    print(f"Clean records: {len(transformed_df)}")
    print(
        f"Rejected/removed records: "
        f"{len(raw_df) - len(transformed_df)}"
    )


if __name__ == "__main__":
    run_pipeline()
