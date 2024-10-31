# 2. Analize SQL și interogări avansate:
import pandas as pd
import mysql.connector
from password import parola

my_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=parola,
    database='ecommerce'
)
cursor = my_db.cursor()


# Venituri lunare si sezoniere
query_orders = 'SELECT * FROM orders'
orders = pd.read_sql(query_orders, my_db)

orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
orders = orders.dropna(subset=['order_date'])
orders['revenue'] = orders['quantity'] * orders['price']
orders['year_month'] = orders['order_date'].dt.to_period('M')

monthly_revenue = orders.groupby('year_month')['revenue'].sum().reset_index()
print(monthly_revenue)


# Analiza produselor populare: Să determine cele mai bine vândute produse din fiecare categorie.
query_products = 'SELECT * FROM products'
cursor.execute(query_products)
products_data = cursor.fetchall()
products_columns = [desc[0] for desc in cursor.description]
products = pd.DataFrame(products_data, columns=products_columns)

merged_data = pd.merge(orders, products, on='product_id')
merged_data['total_sold'] = merged_data['quantity']

popular_products = (
    merged_data.groupby(['category', 'product_name'])['total_sold']
    .sum()
    .reset_index()
    .sort_values(by=['category', 'total_sold'], ascending=[True, False])
    .reset_index(drop=True)
)
print(popular_products)


# Valoarea totala a clientilor: Calculează suma totală a comenzilor fiecărui client.
query_customers = ("SELECT c.name AS customer_name, SUM(o.quantity * o.price) AS total_value "
         "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
         "GROUP BY c.customer_id "
         "ORDER BY total_value DESC")

customer_value = pd.read_sql(query_customers, my_db)
print(customer_value)


