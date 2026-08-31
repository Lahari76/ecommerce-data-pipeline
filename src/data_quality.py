from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
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

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "orders.csv"

def check_required_columns(df: pd.DataFrame):
    """
    Ensure that all required columns are present.
    """
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def check_missing_values(df: pd.DataFrame):
    """
    Check for missing values in critical columns.
    """
    missing_counts = df[REQUIRED_COLUMNS].isnull().sum()
    total_missing = missing_counts.sum()

    if total_missing > 0:
        print("Missing values detected:")
        print(missing_counts[missing_counts > 0])
    else:
        print("No missing values detected.")


def check_duplicate_orders(df: pd.DataFrame):
    """
    Check for duplicate order IDs.
    """
    duplicate_count = df.duplicated(
        subset=["order_id"]
    ).sum()

    if duplicate_count > 0:
        print(
            f"Duplicate order IDs detected: {duplicate_count}"
        )
    else:
        print("No duplicate order IDs detected.")


def check_invalid_values(df: pd.DataFrame):
    """
    Check for invalid quantity and unit price values.
    This includes non-numeric, missing, zero, and negative values.
    """
    quantity = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    unit_price = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    invalid_quantity = (
        quantity.isna() | (quantity <= 0)
    ).sum()

    invalid_price = (
        unit_price.isna() | (unit_price <= 0)
    ).sum()

    if invalid_quantity > 0:
        print(
            f"Invalid quantity records detected: "
            f"{invalid_quantity}"
        )
    else:
        print("No invalid quantity values detected.")

    if invalid_price > 0:
        print(
            f"Invalid unit price records detected: "
            f"{invalid_price}"
        )
    else:
        print("No invalid unit price values detected.")


def run_data_quality_checks(df: pd.DataFrame):
    """
    Run all data-quality checks.
    """
    print("\nRunning data-quality checks...")

    check_required_columns(df)
    check_missing_values(df)
    check_duplicate_orders(df)
    check_invalid_values(df)

    print("Data-quality checks completed.\n")


if __name__ == "__main__":
    df = pd.read_csv(
   	 RAW_DATA_PATH
	)

    run_data_quality_checks(df)
