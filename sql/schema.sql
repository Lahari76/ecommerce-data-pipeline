-- ============================================================
-- E-Commerce Data Engineering Pipeline
-- PostgreSQL Database Schema
-- ============================================================

CREATE TABLE IF NOT EXISTS orders (
    order_id BIGINT PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price > 0),
    order_date DATE NOT NULL,
    country VARCHAR(100) NOT NULL,
    total_amount NUMERIC(14, 2) NOT NULL CHECK (total_amount > 0),
    order_year INTEGER NOT NULL,
    order_month INTEGER NOT NULL CHECK (order_month BETWEEN 1 AND 12),
    order_day INTEGER NOT NULL CHECK (order_day BETWEEN 1 AND 31),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes used for common analytics/filtering operations
CREATE INDEX IF NOT EXISTS idx_orders_customer_id
ON orders(customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_category
ON orders(category);

CREATE INDEX IF NOT EXISTS idx_orders_order_date
ON orders(order_date);
