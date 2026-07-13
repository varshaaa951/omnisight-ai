from database import get_connection, return_connection
from ai import ask_llm


def get_business_data():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    orders = cur.fetchone()[0]

    cur.execute("SELECT SUM(amount) FROM orders")
    revenue = cur.fetchone()[0]

    cur.close()
    return_connection(conn)

    return {
        "customers": customers,
        "orders": orders,
        "revenue": float(revenue)
    }


def get_ai_summary():

    data = get_business_data()

    prompt = f"""
You are an AI Business Analyst.

Current Business Data

Customers : {data['customers']}
Orders : {data['orders']}
Revenue : {data['revenue']}

Generate an executive summary.

Include:

1. Business performance
2. Customer growth
3. Revenue insight
4. One recommendation

Keep it professional.
"""

    return ask_llm(prompt)