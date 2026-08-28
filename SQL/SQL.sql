CREATE DATABASE ecommerce_analytics;
USE ecommerce_analytics;

SELECT DATABASE();

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp VARCHAR(30),
    order_approved_at VARCHAR(30),
    order_delivered_carrier_date VARCHAR(30),
    order_delivered_customer_date VARCHAR(30),
    order_estimated_delivery_date VARCHAR(30)
);

SHOW TABLES;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) AS total_orders
FROM orders;
SELECT *
FROM orders
LIMIT 5;

SELECT COUNT(*) AS total_customers
FROM customers;

SELECT *
FROM customers
LIMIT 5;

SELECT *
FROM order_items
LIMIT 5;


SELECT COUNT(*) AS total_products
FROM products;

SELECT COUNT(*) AS total_payments
FROM payments;

SELECT COUNT(*) AS total_orders
FROM orders;

SHOW TABLES;

SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM orders
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'payments', COUNT(*) FROM payments
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers;


SELECT 
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items;

SELECT COUNT(DISTINCT order_id) AS total_orders
FROM orders;
SELECT   ROUND(SUM(price)/COUNT(DISTINCT order_id) ,2)
AS average_order_value
FROM order_items;


SELECT
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;



SELECT
    ROUND(
        SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS delivered_rate
FROM orders;


SELECT
    o.order_status,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.order_status
ORDER BY revenue DESC;

SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

SELECT
    p.product_category_name,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY revenue DESC
LIMIT 10;

SELECT
    oi.seller_id,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
GROUP BY oi.seller_id
ORDER BY revenue DESC
LIMIT 10;

SELECT
    payment_type,
    ROUND(SUM(payment_value), 2) AS total_payment
FROM payments
GROUP BY payment_type
ORDER BY total_payment DESC;

SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM reviews;

SELECT
    ROUND(
        SUM(CASE WHEN review_score >= 4 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS positive_review_rate
FROM reviews;

SELECT
    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS average_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

SELECT
    COUNT(*) AS orders_over_30_days
FROM orders
WHERE DATEDIFF(
    order_delivered_customer_date,
    order_purchase_timestamp
) > 30;

SELECT
    COUNT(*) AS total_delivered_orders,
    SUM(
        CASE
            WHEN DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            ) > 30 THEN 1
            ELSE 0
        END
    ) AS orders_over_30_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

SELECT
    CASE
        WHEN DATEDIFF(order_delivered_customer_date, order_purchase_timestamp) <= 7
            THEN '0-7 days'
        WHEN DATEDIFF(order_delivered_customer_date, order_purchase_timestamp) <= 14
            THEN '8-14 days'
        WHEN DATEDIFF(order_delivered_customer_date, order_purchase_timestamp) <= 30
            THEN '15-30 days'
        ELSE '30+ days'
    END AS delivery_bucket,
    COUNT(*) AS order_count
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY delivery_bucket
ORDER BY
    CASE delivery_bucket
        WHEN '0-7 days' THEN 1
        WHEN '8-14 days' THEN 2
        WHEN '15-30 days' THEN 3
        WHEN '30+ days' THEN 4
    END;
    
    SELECT
    ROUND(
        AVG(
            TIMESTAMPDIFF(
                HOUR,
                order_purchase_timestamp,
                order_delivered_customer_date
            ) / 24
        ),
        2
    ) AS average_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;


SELECT
    COUNT(*) AS orders_over_30_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
  AND TIMESTAMPDIFF(
        HOUR,
        order_purchase_timestamp,
        order_delivered_customer_date
        ) > 30 * 24;
        
  SELECT
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;      

SELECT
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY order_count DESC;

SELECT
    MAX(order_count) AS maximum_orders_by_one_customer
FROM (
    SELECT
        customer_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
) AS customer_orders;


SELECT
    c.customer_state,
    COUNT(*) AS order_count
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY order_count DESC;

SELECT
    c.customer_state,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC;

SELECT
    c.customer_state,
    ROUND(
        SUM(oi.price) / COUNT(DISTINCT o.order_id),
        2
    ) AS revenue_per_order
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY revenue_per_order DESC;

SELECT
    p.product_category_name,
    COUNT(*) AS units_sold
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY units_sold DESC
LIMIT 10;

SELECT
    p.product_category_name,
    ROUND(AVG(oi.price), 2) AS avg_product_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY avg_product_price DESC
LIMIT 10;

SELECT
    oi.product_id,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
GROUP BY oi.product_id
ORDER BY revenue DESC
LIMIT 10;

SELECT
    s.seller_city,
    s.seller_state,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN sellers s
    ON oi.seller_id = s.seller_id
GROUP BY s.seller_city, s.seller_state
ORDER BY revenue DESC
LIMIT 10;
        
        
        SELECT
    payment_installments,
    COUNT(*) AS payment_count,
    ROUND(SUM(payment_value), 2) AS total_payment
FROM payments
WHERE payment_type = 'credit_card'
GROUP BY payment_installments
ORDER BY payment_installments;



SELECT
    COUNT(*) AS late_deliveries
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
  AND order_delivered_customer_date > order_estimated_delivery_date;
  
  
  WITH category_revenue AS (
    SELECT
        p.product_category_name,
        ROUND(SUM(oi.price), 2) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
)
SELECT
    product_category_name,
    revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM category_revenue
ORDER BY revenue_rank;