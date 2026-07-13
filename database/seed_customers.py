from faker import Faker
import psycopg2

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

cur = conn.cursor()

for i in range(500):
    name = fake.name()
    email = fake.email()

    cur.execute(
        """
        INSERT INTO customers(name, email)
        VALUES (%s, %s)
        """,
        (name, email)
    )

conn.commit()

print("500 customers inserted successfully!")

cur.close()
conn.close()