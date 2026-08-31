import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.append(str(SRC_PATH))

from transform import transform_orders


def test_transform_removes_duplicate_orders():
    df = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": "C001",
            "product_id": "P001",
            "product_name": "Laptop",
            "category": "electronics",
            "quantity": 1,
            "unit_price": 50000,
            "order_date": "2026-08-01",
            "country": "india",
        },
        {
            "order_id": 1,
            "customer_id": "C001",
            "product_id": "P001",
            "product_name": "Laptop",
            "category": "electronics",
            "quantity": 1,
            "unit_price": 50000,
            "order_date": "2026-08-01",
            "country": "india",
        },
    ])

    result = transform_orders(df)

    assert len(result) == 1


def test_transform_removes_missing_customer_id():
    df = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": None,
            "product_id": "P001",
            "product_name": "Laptop",
            "category": "electronics",
            "quantity": 1,
            "unit_price": 50000,
            "order_date": "2026-08-01",
            "country": "india",
        }
    ])

    result = transform_orders(df)

    assert len(result) == 0


def test_transform_removes_invalid_quantity():
    df = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": "C001",
            "product_id": "P001",
            "product_name": "Laptop",
            "category": "electronics",
            "quantity": -1,
            "unit_price": 50000,
            "order_date": "2026-08-01",
            "country": "india",
        }
    ])

    result = transform_orders(df)

    assert len(result) == 0


def test_transform_removes_invalid_unit_price():
    df = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": "C001",
            "product_id": "P001",
            "product_name": "Laptop",
            "category": "electronics",
            "quantity": 1,
            "unit_price": -50000,
            "order_date": "2026-08-01",
            "country": "india",
        }
    ])

    result = transform_orders(df)

    assert len(result) == 0


def test_transform_calculates_total_amount():
    df = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": "C001",
            "product_id": "P001",
            "product_name": "Laptop",
            "category": "electronics",
            "quantity": 2,
            "unit_price": 5000,
            "order_date": "2026-08-01",
            "country": "india",
        }
    ])

    result = transform_orders(df)

    assert result.iloc[0]["total_amount"] == 10000


def test_transform_creates_date_columns():
    df = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": "C001",
            "product_id": "P001",
            "product_name": "Laptop",
            "category": "electronics",
            "quantity": 1,
            "unit_price": 50000,
            "order_date": "2026-08-15",
            "country": "india",
        }
    ])

    result = transform_orders(df)

    assert result.iloc[0]["order_year"] == 2026
    assert result.iloc[0]["order_month"] == 8
    assert result.iloc[0]["order_day"] == 15


def test_transform_standardizes_text():
    df = pd.DataFrame([
        {
            "order_id": 1,
            "customer_id": " C001 ",
            "product_id": " P001 ",
            "product_name": " Laptop ",
            "category": "electronics",
            "quantity": 1,
            "unit_price": 50000,
            "order_date": "2026-08-01",
            "country": "india",
        }
    ])

    result = transform_orders(df)

    assert result.iloc[0]["customer_id"] == "C001"
    assert result.iloc[0]["product_id"] == "P001"
    assert result.iloc[0]["product_name"] == "Laptop"
    assert result.iloc[0]["category"] == "Electronics"
    assert result.iloc[0]["country"] == "India"
