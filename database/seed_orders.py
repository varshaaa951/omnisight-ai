import psycopg2
import random

conn = psycopg2.connect(
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

cur = conn.cursor()

statuses = ["PAID", "PENDING", "CANCELLED"]

for i in range(5000):
    customer_id = random.randint(1, 500)
    amount = round(random.uniform(100, 5000), 2)
    status = random.choice(statuses)

    cur.execute(
        """
        INSERT INTO orders(customer_id, amount, status)
        VALUES (%s, %s, %s)
        """,
        (customer_id, amount, status)
    )

conn.commit()

print("5000 orders inserted successfully!")

cur.close()
conn.close()