import pandas
import mysql.connector
from password import parola
import matplotlib.pyplot as plt

### 1. Extragere
my_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=parola,
    database='ecommerce'
)

cursor = my_db.cursor()
query = 'SELECT c.country, COUNT(o.order_id) AS orders_per_country FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY country LIMIT 10'
df = pandas.read_sql(query, my_db)
print(df)

# fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
#
# df.plot.bar(x='country', y='orders_per_country', ax=axs[0, 0], color='g', alpha=0.7, label='Orderss')
# axs[0, 0].set_title('Orders per country')
#
# axs[0, 1].set_visible(False)
# axs[1, 0].set_visible(False)
# axs[1, 1].set_visible(False)
#
# plt.show()

# # grafic de tip linie
df.plot.bar(x='country', y='orders_per_country', color='g', alpha=0.7, label='Orderss')
plt.xlabel('Country')
plt.ylabel('Orders')
plt.title('Orders per country')
plt.legend()
plt.grid()
plt.show()