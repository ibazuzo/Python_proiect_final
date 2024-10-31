#Punctele 1.1 + 1.2 + 4.1


import pandas as pd
import mysql.connector
from passSQL import parola

# Database connection
my_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=parola,
    database='ecommerce'
)

# Modified query to ensure we get review data
query = """
SELECT DISTINCT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_date,
    o.quantity,
    o.price,

    c.name AS customer_name,
    c.email,
    c.country,
    c.registration_date,

    p.product_name,
    p.category,
    p.stock,

    r.review_id,
    r.rating,
    r.review_date
FROM orders o
LEFT JOIN customers c 
    ON o.customer_id = c.customer_id
LEFT JOIN products p 
    ON o.product_id = p.product_id
LEFT JOIN reviews r 
    ON p.product_id = r.product_id 
    AND o.customer_id = r.customer_id
ORDER BY o.order_id
"""

# Execute the query and load into DataFrame
df_raw = pd.read_sql_query(query, my_db)

# Close the database connection
# my_db.close()

df_raw.to_csv('raw_to_csv', index=False)

# print(df_raw)

valori_lipsa = df_raw.isnull().sum()
# print(valori_lipsa)
df_cu_valori_sterse = df_raw.dropna()
# print(df_cu_valori_sterse)
df_cu_valori_sterse.to_csv()

# Get orders data
query_orders = 'SELECT customer_id, order_id FROM orders'
df_orders = pd.read_sql(query_orders, my_db)

# Get customers data
query_customers = "SELECT customer_id, name FROM customers"
df_customers = pd.read_sql(query_customers, my_db)

# Calculate order counts per customer
df_top10_clients = df_orders.groupby("customer_id").agg({
    'order_id': 'count'
}).reset_index()

# Rename the count column
df_top10_clients = df_top10_clients.rename(columns={'order_id': 'number_of_orders'})

# Sort by number of orders in descending order and get top 10
df_top10_clients = df_top10_clients.sort_values('number_of_orders', ascending=False).head(10)

# Merge with customer names
df_top10_clients = df_top10_clients.merge(
    df_customers[['customer_id', 'name']],
    on='customer_id',
    how='left'
)

# Reorder columns for better readability
df_top10_clients = df_top10_clients[['customer_id', 'name', 'number_of_orders']]

# Display results
print("\nTop 10 Most Active Customers:")
print(df_top10_clients)

# Optional: Create a bar plot of the results
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.bar(df_top10_clients['name'], df_top10_clients['number_of_orders'])
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Customers by Number of Orders')
plt.xlabel('Customer Name')
plt.ylabel('Number of Orders')
plt.tight_layout()
plt.show()