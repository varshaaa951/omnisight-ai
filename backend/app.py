from fastapi import FastAPI
import ollama
import psycopg2
from sentence_transformers import SentenceTransformer

app = FastAPI()

conn = psycopg2.connect(
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)
model = SentenceTransformer("all-MiniLM-L6-v2")
@app.get("/business-summary")
def business_summary():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    orders = cur.fetchone()[0]

    cur.execute("SELECT SUM(amount) FROM orders")
    revenue = cur.fetchone()[0]

    cur.close()

    return {
        "customers": customers,
        "orders": orders,
        "revenue": float(revenue)
    }
@app.get("/ai-business-summary")
def ai_business_summary():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    orders = cur.fetchone()[0]

    cur.execute("SELECT SUM(amount) FROM orders")
    revenue = cur.fetchone()[0]

    cur.close()

    prompt = f"""
    We have:
    Customers: {customers}
    Orders: {orders}
    Revenue: {revenue}

    Give a short business summary.
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"]
    }
@app.get("/ai-business-summary")
def ai_business_summary():
    ...
    return {"answer": response["message"]["content"]}


@app.get("/ask-customers")
def ask_customers():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")

    count = cur.fetchone()[0]

    cur.close()

    prompt = f"""
    We have {count} customers.

    Answer the question:
    How many customers do we have?
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"]
    }
@app.get("/ask/{question}")
def ask(question: str):

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return {
        "question": question,
        "answer": response["message"]["content"]
    }
@app.get("/database-question")
def database_question():

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    customers = cur.fetchone()[0]

    cur.close()

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": f"""
Database Information:
Customers = {customers}

Question:
How many customers do we have?

Answer in one sentence.
"""
            }
        ]
    )

    return {
        "answer": response["message"]["content"]
    }
@app.get("/ask-database/{question}")
def ask_database(question: str):

    cur = conn.cursor()

    if "customer" in question.lower():

        cur.execute("SELECT COUNT(*) FROM customers")
        result = cur.fetchone()[0]

        answer = f"There are {result} customers in the database."

    elif "order" in question.lower():

        cur.execute("SELECT COUNT(*) FROM orders")
        result = cur.fetchone()[0]

        answer = f"There are {result} orders in the database."

    elif "revenue" in question.lower():

        cur.execute("SELECT SUM(amount) FROM orders")
        result = cur.fetchone()[0]

        answer = f"The total revenue is {result}."

    else:

        answer = "Sorry, I can only answer customer, order, or revenue questions right now."

    cur.close()

    return {
        "question": question,
        "answer": answer
    }
@app.get("/rag/{question}")
def rag(question: str):

    query_embedding = model.encode(question).tolist()

    cur = conn.cursor()

    cur.execute("""
    SELECT content
    FROM company_knowledge
    ORDER BY embedding <=> %s::vector
    LIMIT 1;
    """, (query_embedding,))

    knowledge = cur.fetchone()[0]

    cur.close()

    prompt = f"""
    Use this company knowledge:

    {knowledge}

    Answer this question:

    {question}
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "knowledge_used": knowledge,
        "answer": response["message"]["content"]
    }