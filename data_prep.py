import pandas as pd
import mysql.connector
from password import parola

# Conectare la baza de date
my_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=parola,
    database='ecommerce'
)

cursor = my_db.cursor()

#interogare extragere date din DB
query = (
    "SELECT customers.customer_id, customers.name AS customer_name, customers.email, customers.country, "
    "customers.registration_date, products.product_id, products.product_name, products.category, "
    "products.stock, orders.order_id, orders.order_date, orders.quantity, orders.price, reviews.review_id, "
    "reviews.rating, reviews.review_date "
    "FROM ecommerce.customers "
    "JOIN ecommerce.orders ON customers.customer_id = orders.customer_id "
    "JOIN ecommerce.products ON orders.product_id = products.product_id "
    "LEFT JOIN ecommerce.reviews ON customers.customer_id = reviews.customer_id "
    "AND products.product_id = reviews.product_id;"
)
query_customers = (
    "SELECT customer_id, name, email, country, registration_date "
    "FROM ecommerce.customers;")
query_products = (
    "SELECT product_id, product_name, category, stock "
    "FROM ecommerce.products;")
query_orders = (
    "SELECT order_id, customer_id, product_id, order_date, quantity, price "
    "FROM ecommerce.orders;")
query_reviews = (
    "SELECT review_id, customer_id, product_id, rating, review_date "
    "FROM ecommerce.reviews;")

df_c = pd.read_sql_query(query_customers, my_db)
df_p = pd.read_sql_query(query_products, my_db)
df_o = pd.read_sql_query(query_orders, my_db)
df_r = pd.read_sql_query(query_reviews, my_db)
df = pd.read_sql_query(query, my_db)

# verificam valorile lipsa
df_clean_c = df_c.dropna()
df_clean_p = df_p.dropna()
df_clean_o = df_o.dropna()
df_clean_r = df_r.dropna()

# Join intre tabelele curatate
# Join intre customers si orders pe baza customer_id
df_customers_orders = pd.merge(df_clean_c, df_clean_o, on='customer_id', how='inner')

# Join intre customers_orders si products pe baza product_id
df_customers_orders_products = pd.merge(df_customers_orders, df_clean_p, on='product_id', how='inner')

# Join intre customers_orders_products si reviews pe baza customer_id si product_id
df_final = pd.merge(df_customers_orders_products, df_clean_r, on=['customer_id', 'product_id'], how='left')

df_final.to_csv('clean_data.csv', index=False)
