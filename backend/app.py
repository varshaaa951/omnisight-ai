from rag import rag_answer
from summary import get_business_data, get_ai_summary
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_connection, return_connection
from ai import ask_llm, model

app = FastAPI(title="OmniSight AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to OmniSight AI 🚀"
    }


@app.get("/analytics")
def analytics():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    orders = cur.fetchone()[0]

    cur.close()
    return_connection(conn)

    return {
        "chart_type": "BAR",
        "labels": ["Customers", "Orders"],
        "values": [customers, orders]
    }


@app.get("/ask/{question}")
def ask(question: str):

    answer = ask_llm(question)

    return {
        "question": question,
        "answer": answer
    }
@app.get("/business-summary")
def business_summary():

    return get_business_data()


@app.get("/ai-business-summary")
def ai_business_summary():

    return {
        "summary": get_ai_summary()
    }
@app.get("/rag/{question}")
def rag(question: str):

    return {
        "question": question,
        "answer": rag_answer(question)
    }
from summary import get_business_data, get_ai_summary


@app.get("/executive-report")
def executive_report():

    data = get_business_data()

    summary = get_ai_summary()

    return {
        "generated_at": "2026-07-03",
        "statistics": data,
        "executive_summary": summary
    }
@app.get("/dashboard")
def dashboard():

    data = get_business_data()

    return data
@app.get("/customers")
def customers():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM customers LIMIT 100")

    columns = [desc[0] for desc in cur.description]

    rows = cur.fetchall()

    cur.close()
    return_connection(conn)

    return [dict(zip(columns,row)) for row in rows]
@app.get("/orders")
def orders():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders LIMIT 100")

    columns = [desc[0] for desc in cur.description]

    rows = cur.fetchall()

    cur.close()
    return_connection(conn)

    return [dict(zip(columns,row)) for row in rows]
@app.get("/dashboard")
def dashboard():

    data = get_business_data()

    return data
@app.get("/customers")
def customers():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM customers LIMIT 100")

    columns = [desc[0] for desc in cur.description]

    rows = cur.fetchall()

    cur.close()
    return_connection(conn)

    return [dict(zip(columns,row)) for row in rows]
@app.get("/orders")
def orders():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders LIMIT 100")

    columns = [desc[0] for desc in cur.description]

    rows = cur.fetchall()

    cur.close()
    return_connection(conn)

    return [dict(zip(columns,row)) for row in rows]


