from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI
from database import conn
from ai import model, ask_llm

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    question: str

from database import conn
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

    answer = ask_llm(prompt)

    return {
        "answer": answer
    }
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

    answer = ask_llm(question)

    return {
        "question": question,
        "answer": answer
    }

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
@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question

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
        "answer": response["message"]["content"]
    }
