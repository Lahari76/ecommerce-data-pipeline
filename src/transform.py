import pandas as pd
from pathlib import Path

from extract import extract_orders


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "orders_cleaned.csv"

def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform raw e-commerce order data.
    """

    print("Starting data transformation...")

    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Remove duplicate orders based on order_id
    df = df.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

    # Critical columns required for a valid order
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

    # Remove rows with missing critical values
    df = df.dropna(subset=required_columns)

    # Convert numeric columns
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    # Convert order_date to datetime
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Remove rows that became invalid during type conversion
    df = df.dropna(
        subset=[
            "quantity",
            "unit_price",
            "order_date"
        ]
    )

    # Remove invalid business values
    df = df[
        (df["quantity"] > 0)
        & (df["unit_price"] > 0)
    ]

    # Standardize text columns
    df["customer_id"] = (
        df["customer_id"]
        .astype(str)
        .str.strip()
    )

    df["product_id"] = (
        df["product_id"]
        .astype(str)
        .str.strip()
    )

    df["product_name"] = (
        df["product_name"]
        .astype(str)
        .str.strip()
    )

    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df["country"] = (
        df["country"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Calculate total order amount
    df["total_amount"] = (
        df["quantity"] * df["unit_price"]
    )

    # Create date-derived columns
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["order_day"] = df["order_date"].dt.day

    # Reset DataFrame index after removing invalid records
    df = df.reset_index(drop=True)

    print("Data transformation completed successfully.")
    print(f"Number of transformed records: {len(df)}")

    return df


def save_transformed_data(df: pd.DataFrame):
    """
    Save cleaned and transformed data to the processed directory.
    """

    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print(
        f"Processed data saved to: "
        f"{PROCESSED_DATA_PATH}"
    )


if __name__ == "__main__":

    # Extract raw data
    raw_df = extract_orders()

    # Transform raw data
    transformed_df = transform_orders(raw_df)

    # Save processed data
    save_transformed_data(transformed_df)

    # Display sample transformed records
    print("\nSample transformed records:")
    print(transformed_df.head())
