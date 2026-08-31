-- ============================================================
-- E-Commerce Data Engineering Pipeline
-- Analytical SQL Queries
-- ============================================================


-- 1. Overall sales summary
SELECT
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders;


-- 2. Revenue by category
SELECT
    category,
    COUNT(*) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM orders
GROUP BY category
ORDER BY total_revenue DESC;


-- 3. Top 5 products by revenue
SELECT
    product_name,
    category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM orders
GROUP BY product_name, category
ORDER BY total_revenue DESC
LIMIT 5;


-- 4. Revenue by customer
SELECT
    customer_id,
    COUNT(*) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;


-- 5. Daily sales performance
SELECT
    order_date,
    COUNT(*) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS daily_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;


-- 6. Monthly sales performance
SELECT
    order_year,
    order_month,
    COUNT(*) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS monthly_revenue
FROM orders
GROUP BY order_year, order_month
ORDER BY order_year, order_month;


-- 7. Country-wise sales
SELECT
    country,
    COUNT(*) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM orders
GROUP BY country
ORDER BY total_revenue DESC;


-- 8. Customers with multiple orders
SELECT
    customer_id,
    COUNT(*) AS order_count,
    ROUND(SUM(total_amount), 2) AS total_spent
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY total_spent DESC;
