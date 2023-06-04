WITH weekly_sales AS (
    SELECT
        p.category,
        o.product_id,
        o.customer_id,
        SUM(o.quantity) AS total_sales
    FROM
        orders o
        JOIN products p ON o.product_id = p.product_id
    WHERE
        o.order_time >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 WEEK) -- Filter for the last week
    GROUP BY
        p.category,
        o.product_id,
        o.customer_id
), top_products AS (
    SELECT
        category,
        product_id,
        customer_id,
        total_sales,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_sales DESC) AS ranks
    FROM
        weekly_sales
    WHERE
       total_sales >= 100 -- Filter for categories with total sales >= 100 units
), recent_customers AS (
    SELECT
        customer_id
    FROM
        customers
    WHERE
        customer_datetime >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) -- Filter for customers registered in the past year
) 
	SELECT
		p.category,
		p.product_name,
		tp.total_sales
	FROM
		top_products tp
		JOIN products p ON tp.product_id = p.product_id
		JOIN recent_customers rc ON tp.customer_id = rc.customer_id
	WHERE
		tp.ranks <= 3 -- Retrieve the top 3 products in each category
	ORDER BY
		p.category,
		tp.total_sales DESC;