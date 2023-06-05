WITH weekly_sales AS (
    SELECT
        p.category,
        o.product_id,
        SUM(o.quantity) AS total_sales
    FROM
        orders o
        JOIN products p ON o.product_id = p.product_id
        JOIN customers c ON o.customer_id = c.customer_id
    WHERE
        o.order_time >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) -- Filter for the last week
        AND c.registration_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) -- Filter for customers registered in the past year
    GROUP BY
        p.category,
        o.product_id
),
category_sales AS (
    SELECT
        category,
        product_id,
        total_sales,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_sales DESC) AS rn
    FROM
        weekly_sales
),
filtered_categories AS (
    SELECT
        category
    FROM
        weekly_sales
    GROUP BY
        category
    HAVING
        SUM(total_sales) < 100
)
SELECT
    cs.category,
    cs.product_id,
    cs.total_sales
FROM
    category_sales cs
    JOIN filtered_categories fc ON cs.category = fc.category
WHERE
    cs.rn <= 3 -- Retrieve the top 3 products in each category
ORDER BY
    cs.category,
    cs.total_sales DESC;
