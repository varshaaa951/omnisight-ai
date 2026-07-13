import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

cur = conn.cursor()

# Customers
cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]

# Orders
cur.execute("SELECT COUNT(*) FROM orders")
orders = cur.fetchone()[0]

# Revenue
cur.execute("SELECT SUM(amount) FROM orders")
revenue = cur.fetchone()[0]

print("Customers:", customers)
print("Orders:", orders)
print("Revenue:", revenue)

cur.close()
conn.close()