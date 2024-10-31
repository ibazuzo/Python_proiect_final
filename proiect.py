import matplotlib.pyplot as plot
import pandas
import pandas as pd
import numpy as np
import datetime

import mysql.connector
from password import parola

my_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=parola,
    database='ecommerce'
)
cursor=my_db.cursor()
cursor.execute('SHOW TABLES')
for x in cursor:
    print(x)

#grafic tip linie
query_orders = 'SELECT COUNT(order_id) AS orders_number, order_date FROM orders GROUP BY order_date ORDER BY order_date ASC LIMIT 10'
orders = pandas.read_sql(query_orders, my_db)
print(orders)

orders.plot(x='order_date', y='orders_number', marker='o', linestyle='-', color='b', label='order_date')
plot.xlabel('orders_number')
plot.ylabel('order_date')
plot.title('Tendinte de vanzari sezoniere')
plot.legend()
plot.grid()
plot.show()

#grafic tip bara
