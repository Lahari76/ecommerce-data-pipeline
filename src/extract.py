import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "orders.csv"

def extract_orders():
    """
    Extract raw e-commerce order data from CSV.
    """

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_DATA_PATH}"
        )

    df = pd.read_csv(RAW_DATA_PATH)

    print("Data extraction completed successfully.")
    print(f"Number of records extracted: {len(df)}")

    return df


if __name__ == "__main__":
    orders_df = extract_orders()
    print(orders_df.head())
