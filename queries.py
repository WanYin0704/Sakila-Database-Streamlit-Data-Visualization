#--- PART A---

#Overview
queryT1 = 'SELECT count(*) FROM customers'
queryT2 = 'SELECT count(DISTINCT(product_name)) FROM products'
queryT3 = 'SELECT count(*) FROM stores'
queryT4 = 'SELECT count(*) FROM orders'
queryT5 = 'SELECT YEAR(order_Date) as year,  count(*) as no_of_orders FROM orders GROUP BY YEAR(order_Date)'
queryT6 = 'SELECT store_id as store, count(*) as no_of_orders FROM orders GROUP BY store_id'

#------Customer------
# Categorize customers into One-Time or Recurring based on the number of orders
query_customer_category = '''
   SELECT
    customer_category,
    COUNT(customer_id) AS customer_count
FROM
    (
        SELECT
            c.customer_id,
            CASE
                WHEN COUNT(o.order_id) = 1 THEN 'One-Time'
                ELSE 'Recurring'
            END as customer_category
        FROM
            customers c
        LEFT JOIN
            orders o ON c.customer_id = o.customer_id
        GROUP BY
            c.customer_id
    ) AS customer_categories
GROUP BY
    customer_category;
'''

# List of recurring customers and their corresponding sales
query_recurring_customers = '''
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        COUNT(DISTINCT o.order_id) as order_count,
        SUM(oi.list_price * oi.quantity * (1 - oi.discount)) as total_sales
    FROM
        customers c
    JOIN
        orders o ON c.customer_id = o.customer_id
    JOIN
        order_items oi ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id
    HAVING
        order_count > 1
    ORDER BY
        total_sales DESC
'''


# List of top 10 customers who spent the most
query_top_spenders = '''
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        COUNT(DISTINCT o.order_id) as order_count,
        SUM(oi.list_price * oi.quantity * (1 - oi.discount)) as total_spending
    FROM
        customers c
    JOIN
        orders o ON c.customer_id = o.customer_id
    JOIN
        order_items oi ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id
    ORDER BY
        total_spending DESC
    LIMIT 10
'''

#-----Order-----
queryO1 = 'SELECT (SUM(quantity*list_price*(1-discount))) AS total_sales FROM order_items;'

queryS2='SELECT YEAR(o.order_date)AS year, p.product_name, SUM(oi.list_price * oi.quantity * (1 - oi.discount)) AS product_sales FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY year,p.product_name'

query_sale_by_year='SELECT YEAR(o.order_date)AS year, SUM(oi.list_price * oi.quantity * (1 - oi.discount)) AS total_sales FROM orders o JOIN order_items oi ON o.order_id = oi.order_id GROUP BY YEAR(o.order_date) '

queryO3 = 'SELECT p.product_id, p.product_name, SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales FROM order_items oi JOIN products p  ON oi.product_id = p.product_id GROUP BY p.product_id ORDER BY total_sales DESC LIMIT 1;'


#-----Staff-----
queryO4 = 'SELECT s.store_name, COUNT(*) AS total_staff FROM staffs st JOIN stores s ON s.store_id = st.store_id GROUP BY store_name;'

queryO5 = 'SELECT s.store_name, COUNT(DISTINCT c.customer_id) AS total_customers, COUNT(DISTINCT st.staff_id) AS total_staff, COUNT(DISTINCT c.customer_id) / COUNT(DISTINCT st.staff_id) AS customer_staff_ratio FROM orders o JOIN stores s ON o.store_id = s.store_id JOIN customers c ON c.customer_id = o.customer_id JOIN staffs st ON st.staff_id = o.staff_id GROUP BY o.store_id;'

queryO6 = 'SELECT s.store_name, YEAR(o.order_date), COUNT(DISTINCT c.customer_id) AS total_customers, COUNT(DISTINCT st.staff_id) AS total_staff, COUNT(DISTINCT c.customer_id) / COUNT(DISTINCT st.staff_id) AS customer_staff_ratio FROM orders o JOIN stores s ON o.store_id = s.store_id JOIN customers c ON c.customer_id = o.customer_id JOIN staffs st ON st.staff_id = o.staff_id GROUP BY o.store_id, YEAR(o.order_date);'


#-----Items-----
queryP1='SELECT COUNT(DISTINCT(product_name)) AS total_products, COUNT(DISTINCT brand_id) AS total_brands FROM products'

queryP2='SELECT b.brand_name, COUNT(DISTINCT(product_name)) AS product_count FROM brands b JOIN products p ON b.brand_id = p.brand_id GROUP BY b.brand_name ORDER BY product_count DESC'

queryP3='SELECT b.brand_name, SUM(oi.list_price * oi.quantity * (1 - oi.discount)) AS total_sales, p.product_name FROM brands b JOIN products p ON b.brand_id = p.brand_id JOIN order_items oi ON p.product_id = oi.product_id GROUP BY b.brand_name, p.product_name ORDER BY total_sales DESC LIMIT 1'

queryP4='SELECT DISTINCT(p.product_name), CASE WHEN p.list_price < 500 THEN "Low-priced" WHEN p.list_price BETWEEN 500 AND 1000 THEN "Medium-priced" ELSE "High-priced" END AS price_category, SUM(oi.list_price * oi.quantity * (1 - oi.discount)) AS total_sales FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_name, price_category ORDER BY price_category,total_sales DESC;'

query_no_item_category='''SELECT
    price_category,
    COUNT(product_name) AS product_count
FROM
    (
        SELECT
            p.product_name,
            CASE
                WHEN p.list_price < 500 THEN 'Low-priced'
                WHEN p.list_price BETWEEN 500 AND 1000 THEN 'Medium-priced'
                ELSE 'High-priced'
            END AS price_category,
            SUM(oi.list_price * oi.quantity * (1 - oi.discount)) AS total_sales
        FROM
            products p
        JOIN
            order_items oi ON p.product_id = oi.product_id
        GROUP BY
            p.product_name, price_category
    ) AS products_per_category
GROUP BY
    price_category;
'''

queryLow='SELECT p.product_id, p.product_name, p.list_price, SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_name, p.list_price HAVING p.list_price < 500 ORDER BY total_sales DESC LIMIT 5'

queryMed='SELECT p.product_id, p.product_name, p.list_price, SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY  p.product_name, p.list_price HAVING p.list_price BETWEEN 500 AND 1000  ORDER BY total_sales DESC LIMIT 5'

queryHigh='SELECT p.product_id, p.product_name, p.list_price, SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_name, p.list_price HAVING p.list_price > 1000  ORDER BY total_sales DESC LIMIT 5'


#--- PART B---

#-----Overview-----
query1='SELECT count(*) FROM customer WHERE Active=1'

query2='SELECT count(*) FROM store'

query3='SELECT count(*) FROM staff'

query4='SELECT count(*) FROM film'

query5='SELECT count(*) FROM actor'

# WHERE active=1 ==> Active cust
query6 =""" SELECT 
        store_id,
        COUNT(*) AS customer_count
    FROM 
        customer
    WHERE active=1
    GROUP BY 
        store_id;
"""

#  WHERE late_payment_fee= p.amount-f.rental_rate > 0
query7='''SELECT COUNT(r.customer_id)as total_late_payment_cust, f.title as film_title
    FROM film f 
        JOIN inventory i ON f.film_id=i.film_id 
        JOIN rental r ON i.inventory_id=r.inventory_id  
        JOIN payment p ON r.rental_id=p.rental_id 
    WHERE p.amount- f.rental_rate > 0
    GROUP BY film_title'''

#  WHERE late_payment_fee= p.amount-f.rental_rate > 0
# GROUP BY category
query_total_late_cust="""SELECT
    cat.name as category,
    COUNT(r.customer_id) AS sum_late_payment_cust
FROM
    film f
JOIN
    inventory i ON f.film_id = i.film_id
JOIN
    rental r ON i.inventory_id = r.inventory_id
JOIN
    payment p ON r.rental_id = p.rental_id
JOIN
    customer c ON p.customer_id = c.customer_id
JOIN
    film_category fc ON f.film_id = fc.film_id
JOIN
    category cat ON fc.category_id = cat.category_id
WHERE
    p.amount - f.rental_rate > 0
GROUP BY
    cat.name;"""


#-----Sales-----
query8='SELECT SUM(p.amount- f.rental_rate) as overall_sum_late_payment FROM film f join inventory i ON f.film_id=i.film_id JOIN rental r ON i.inventory_id=r.inventory_id  JOIN payment p ON r.rental_id=p.rental_id WHERE p.amount- f.rental_rate > 0'
query9='SELECT SUM(p.amount) as total_sales FROM payment p'
query10='SELECT AVG(p.amount) as avg_sales FROM payment p'
query11='SELECT YEAR(payment_date) as year, SUM(amount) as annual_sales FROM payment GROUP BY YEAR(payment_date)'
query21='SELECT YEAR(payment_date) as year, MONTH(payment_date) as month, SUM(amount) as monthly_sales FROM payment GROUP BY YEAR(payment_date), MONTH(payment_date);'
query31='SELECT c.name as name, SUM(p.amount) as total_sales_per_category FROM film_category fc JOIN category c ON fc.category_id = c.category_id JOIN film f ON fc.film_id = f.film_id JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id JOIN payment p ON r.rental_id = p.rental_id GROUP BY c.name'
query41='SELECT f.rating, SUM(p.amount) as total_sales_by_rating FROM film f JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id JOIN payment p ON r.rental_id = p.rental_id GROUP BY f.rating'
query42 = 'SELECT cty.country as Country, SUM(p.amount) as total_sales_per_country FROM customer c JOIN payment p ON c.customer_id = p.customer_id JOIN address a ON c.address_id = a.address_id JOIN city ct ON a.city_id = ct.city_id JOIN country cty ON ct.country_id = cty.country_id GROUP BY cty.country ORDER BY total_sales_per_country DESC LIMIT 10;'
query43 = 'SELECT cty.country, ct.city, SUM(p.amount) as total_sales_per_country FROM customer c JOIN payment p ON c.customer_id = p.customer_id JOIN address a ON c.address_id = a.address_id JOIN city ct ON a.city_id = ct.city_id JOIN country cty ON ct.country_id = cty.country_id GROUP BY cty.country, ct.city;' 


#-----Film-----
queryF4='SELECT AVG(length) FROM film'

queryF5='SELECT COUNT(DISTINCT(category_id)) from category'

queryF6='SELECT DISTINCT(l.name) FROM language l JOIN film f ON l.language_id=f.language_id'

queryF7='SELECT c.name as category, COUNT(film_id) as num_film FROM film_category fc JOIN category c ON fc.category_id = c.category_id GROUP BY c.name'

queryF8='''SELECT f.title, COUNT(r.rental_id) as rental_count 
    FROM film f 
        JOIN inventory i ON f.film_id = i.film_id 
        JOIN rental r ON i.inventory_id = r.inventory_id 
    GROUP BY f.title 
    ORDER BY rental_count DESC LIMIT 10'''

queryF9='SELECT DISTINCT(release_year) FROM film'

queryF10='''SELECT f.rating as ratings, COUNT(f.film_id) as no_film 
    FROM film f 
        JOIN inventory i ON f.film_id = i.film_id 
        JOIN rental r ON i.inventory_id = r.inventory_id 
        JOIN payment p ON r.rental_id = p.rental_id 
    GROUP BY f.rating'''

queryF11='SELECT special_features as special_features, COUNT(film_id) as film_count FROM film GROUP BY special_features'


#Actor
q1= """
SELECT a.actor_id, CONCAT(a.first_name, ' ', a.last_name) AS actor_name, COUNT(fa.film_id) as film_count
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id
ORDER BY COUNT(fa.film_id) DESC
LIMIT 10;
"""

q2 = "SELECT COUNT(*) FROM actor;"


q3 = """
SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor_name
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id
ORDER BY COUNT(fa.film_id) DESC
LIMIT 1;
"""

q4 = """
SELECT 
    CONCAT(a.first_name, ' ', a.last_name) AS actor_name, 
    c.name AS category_name, 
    COUNT(*) AS film_count
FROM 
    actor a
JOIN 
    film_actor fa ON a.actor_id = fa.actor_id
JOIN 
    film_category fc ON fa.film_id = fc.film_id
JOIN 
    category c ON fc.category_id = c.category_id
GROUP BY 
    a.actor_id, c.category_id;
"""

q5 = """
SELECT 
    actor_name, 
    release_year, 
    film_count
FROM (
    SELECT 
        CONCAT(a.first_name, ' ', a.last_name) AS actor_name, 
        f.release_year,
        COUNT(*) AS film_count,
        RANK() OVER (PARTITION BY f.release_year ORDER BY COUNT(*) DESC) as `rank`
    FROM 
        actor a
    JOIN 
        film_actor fa ON a.actor_id = fa.actor_id
    JOIN 
        film f ON fa.film_id = f.film_id
    GROUP BY 
        a.actor_id, f.release_year
    ) as ranked_actors
WHERE 
    `rank` <= 5;
"""

q6 = """
SELECT 
    CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
    AVG(CAST(f.length AS FLOAT)) AS avg_film_length
FROM 
    actor a
JOIN 
    film_actor fa ON a.actor_id = fa.actor_id
JOIN 
    film f ON fa.film_id = f.film_id
GROUP BY 
    a.actor_id
ORDER BY 
    avg_film_length DESC
LIMIT 10;
"""

q7 = """
SELECT 
    c.name AS category_name,
    COUNT(DISTINCT a.actor_id) AS actor_count
FROM 
    category c
JOIN 
    film_category fc ON c.category_id = fc.category_id
JOIN 
    film_actor fa ON fc.film_id = fa.film_id
JOIN 
    actor a ON fa.actor_id = a.actor_id
GROUP BY 
    c.name;
"""


#Rental

# Query 1: Total Rental Counts
queryR1 = 'SELECT COUNT(rental_id) FROM rental'

# Query 2: Average Rental Duration
queryR2 = 'SELECT AVG(rental_duration) FROM film'

# Query 3: Rentals by Category
queryR3 = 'SELECT c.name AS category, COUNT(r.rental_id) AS rental_count FROM rental r JOIN inventory i ON r.inventory_id = i.inventory_id JOIN film_category fc ON i.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id GROUP BY c.name'

# Query 4: Average Rental Rate by Category
queryR4 = 'SELECT c.name AS category, AVG(f.rental_rate) AS avg_rental_rate FROM film f JOIN film_category fc ON f.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id GROUP BY c.name'

#histogram Rental Duration Distribution
rental_duration_category_query = '''
SELECT
    c.name AS category,
    SUM(TIMESTAMPDIFF(HOUR, r.rental_date, r.return_date)) AS total_rental_duration
FROM
    rental r
JOIN
    inventory i ON r.inventory_id = i.inventory_id
JOIN
    film_category fc ON i.film_id = fc.film_id
JOIN
    category c ON fc.category_id = c.category_id
WHERE
    r.return_date IS NOT NULL
GROUP BY
    c.name;

    '''


# Query 5: Loyal Customers
queryR5 = 'SELECT c.customer_id, c.first_name AS first_name, c.last_name AS last_name, COUNT(r.rental_id) AS rental_count FROM customer c JOIN rental r ON c.customer_id = r.customer_id GROUP BY c.customer_id HAVING rental_count > 1 ORDER BY COUNT(r.rental_id) DESC LIMIT 10'

# Query 6: Distribution of Rental Counts by Store
queryR6 = 'SELECT s.store_id as store, COUNT(r.rental_id) AS rental_count FROM rental r JOIN staff s ON r.staff_id = s.staff_id GROUP BY s.store_id'

# Query 7: Rental Counts by Language
queryR7 = '''
SELECT
    l.name AS language,
    COUNT(r.rental_id) AS rental_count
FROM
    rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN language l ON f.language_id = l.language_id
GROUP BY
    l.name
'''

# Query 8: Top 10 Renting Films by Rental Rate
queryR8 = '''
SELECT
    f.title AS film_title,
    AVG(f.rental_rate) AS avg_rental_rate
FROM
    rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
GROUP BY
    f.title
ORDER BY
    avg_rental_rate DESC
;
'''

# Query 9: Rental Revenue Over Time
queryR9 = '''
SELECT
    rental_date,
    SUM(amount) AS revenue
FROM
    rental r
    JOIN payment p ON r.rental_id = p.rental_id
GROUP BY
    rental_date
ORDER BY
    rental_date
'''










