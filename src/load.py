from pathlib import Path
import os
import psycopg2
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "orders_cleaned.csv"

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "ecommerce_db"),
    "user": os.getenv("DB_USER", "ecommerce_user"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5433"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def load_to_postgres(df):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        print("PostgreSQL connection established successfully.")

        insert_query = """
        INSERT INTO orders (
            order_id,
            customer_id,
            product_id,
            product_name,
            category,
            quantity,
            unit_price,
            order_date,
            country,
            total_amount,
            order_year,
            order_month,
            order_day
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (order_id)
        DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            product_id = EXCLUDED.product_id,
            product_name = EXCLUDED.product_name,
            category = EXCLUDED.category,
            quantity = EXCLUDED.quantity,
            unit_price = EXCLUDED.unit_price,
            order_date = EXCLUDED.order_date,
            country = EXCLUDED.country,
            total_amount = EXCLUDED.total_amount,
            order_year = EXCLUDED.order_year,
            order_month = EXCLUDED.order_month,
            order_day = EXCLUDED.order_day;
        """

        records = [
            (
                int(row.order_id),
                row.customer_id,
                row.product_id,
                row.product_name,
                row.category,
                int(row.quantity),
                float(row.unit_price),
                row.order_date,
                row.country,
                float(row.total_amount),
                int(row.order_year),
                int(row.order_month),
                int(row.order_day),
            )
            for row in df.itertuples(index=False)
        ]

        cursor.executemany(insert_query, records)
        connection.commit()

        print(f"Successfully loaded {len(records)} records into PostgreSQL.")

    except Exception as error:
        if connection:
            connection.rollback()

        print(f"PostgreSQL load failed: {error}")
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
            print("PostgreSQL connection closed.")


if __name__ == "__main__":
    processed_file = PROCESSED_DATA_PATH

    print(f"Reading processed data from: {processed_file}")

    dataframe = pd.read_csv(processed_file)

    load_to_postgres(dataframe)
