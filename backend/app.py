from fastapi import FastAPI
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

@app.get("/")
def home():
    return {"message": "OmniSight AI Backend Running"}

@app.get("/customers/count")
def customers_count():

    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM customers"
    )

    count = cur.fetchone()[0]

    cur.close()

    return {
        "total_customers": count
    }

@app.get("/orders/count")
def orders_count():

    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM orders"
    )

    count = cur.fetchone()[0]

    cur.close()

    return {
        "total_orders": count
    }
@app.get("/orders/revenue")
def orders_revenue():

    cur = conn.cursor()

    cur.execute(
        "SELECT SUM(amount) FROM orders"
    )

    count = cur.fetchone()[0]

    cur.close()

    return {
        "total_revenue": count
    }
@app.get("/orders/average")
def orders_average():

    cur = conn.cursor()

    cur.execute(
        "SELECT AVG(amount) FROM orders"
    )

    count = cur.fetchone()[0]

    cur.close()

    return {
        "average_order_value": count
    }
@app.get("/orders/status-summary")
def status_summary():

    cur = conn.cursor()

    cur.execute("""
        SELECT status, COUNT(*)
        FROM orders
        GROUP BY status
    """)

    rows = cur.fetchall()

    result = {}

    for status, count in rows:
        result[status] = count

    cur.close()
    print(result)

    return result
