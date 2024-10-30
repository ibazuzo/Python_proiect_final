# 2. Analize SQL și interogări avansate:
# o Venituri lunare și sezoniere: O interogare SQL care returnează veniturile
# totale pe lună pentru a analiza sezonalitatea.
# o Analiza produselor populare: Să determine cele mai bine vândute produse
# din fiecare categorie.
# o Valoarea totală a clienților (Customer Lifetime Value): Calculează suma
# totală a comenzilor fiecărui client.
# o Recenzii și satisfacția clienților: O interogare care determină media
# ratingurilor pe produs pentru a vedea care produse au cea mai mare satisfacție.
# o Top 5 clienți fideli: Identificarea clienților cu cele mai multe comenzi plasate.

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
# query_orders = 'SELECT * FROM orders'
# orders = pd.read_sql(query_orders, my_db)
# print(orders)
#
# orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
#
# orders = orders.dropna(subset=['order_date'])
#
# orders['revenue'] = orders['quantity'] * orders['price']
#
# orders['year_month'] = orders['order_date'].dt.to_period('M')
#
# monthly_revenue = orders.groupby('year_month')['revenue'].sum().reset_index()
#
# print(monthly_revenue)

# Analiza produselor populare: Să determine cele mai bine vândute produse din fiecare categorie.
query_products = 'SELECT * FROM products'
products = pd.read_sql(query_products, my_db)
print(products)
query_product_sales =  'SELECT p.category, p.Product_name, SUM(o.quantity) as total_sold FROM orders o JOIN products p ON o.product_id = p.product_id GROUP BY p.category, p.product_name ORDER BY total_sold DESC'
popular_products = pd.read_sql(query_product_sales, my_db)
print(popular_products)



# Valoarea totala a clientilor
# query_products = 'SELECT * FROM customers'
# customers = pd.read_sql(query_products, my_db)
# print(customers)
# query_client_orders = 'SELECT c.customer_id, c.name, SUM(o.price * o.quantity) as total_value FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name ORDER BY total_value DESC'
# top_clients_orders = pd.read_sql(query_client_orders, my_db)
# print(top_clients_orders)


# Recenzii si satisfactia clientilor


# Top 5 clienti fideli
