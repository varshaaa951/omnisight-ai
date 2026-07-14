from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_connection, return_connection
from ai import ask_llm
from summary import get_business_data, get_ai_summary
from rag import rag_answer
from cross_database_query import run_cross_database_query

app = FastAPI(
    title="OmniSight AI",
    version="1.0.0",
    description="AI Powered Business Intelligence Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


# -------------------------------------------------
# Home
# -------------------------------------------------

@app.get("/")
def home():

    return {
        "application": "OmniSight AI",
        "status": "Running",
        "version": "1.0",
        "message": "Welcome to OmniSight AI 🚀"
    }


# -------------------------------------------------
# Analytics
# -------------------------------------------------

@app.get("/analytics")
def analytics():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("SELECT COUNT(*) FROM customers")
        customers = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM orders")
        orders = cur.fetchone()[0]

        return {
            "chart_type": "BAR",
            "labels": ["Customers", "Orders"],
            "values": [customers, orders]
        }

    finally:
        cur.close()
        return_connection(conn)


# -------------------------------------------------
# General AI Chat
# -------------------------------------------------

@app.get("/ask/{question}")
def ask(question: str):

    answer = ask_llm(question)

    return {
        "question": question,
        "answer": answer
    }


@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask_llm(request.question)

    return {
        "question": request.question,
        "answer": answer
    }
# -------------------------------------------------
# Business Summary
# -------------------------------------------------

@app.get("/business-summary")
def business_summary():

    return get_business_data()


@app.get("/ai-business-summary")
def ai_business_summary():

    return {
        "summary": get_ai_summary()
    }


# -------------------------------------------------
# Retrieval Augmented Generation (RAG)
# -------------------------------------------------

@app.get("/rag/{question}")
def rag(question: str):

    return {
        "question": question,
        "answer": rag_answer(question)
    }


# -------------------------------------------------
# Executive Report
# -------------------------------------------------

@app.get("/executive-report")
def executive_report():

    data = get_business_data()

    summary = get_ai_summary()

    return {
        "generated_at": "2026-07-14",
        "statistics": data,
        "executive_summary": summary
    }


# -------------------------------------------------
# Dashboard
# -------------------------------------------------

@app.get("/dashboard")
def dashboard():

    return get_business_data()
# -------------------------------------------------
# Customers
# -------------------------------------------------

@app.get("/customers")
def customers():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT *
            FROM customers
            LIMIT 100
        """)

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:
        cur.close()
        return_connection(conn)


# -------------------------------------------------
# Orders
# -------------------------------------------------

@app.get("/orders")
def orders():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT *
            FROM orders
            LIMIT 100
        """)

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:
        cur.close()
        return_connection(conn)


# -------------------------------------------------
# Cross Database Integration
# (Phase 3.4)
# -------------------------------------------------

@app.get("/cross-database")
def cross_database():

    result = run_cross_database_query()

    result = result.astype(object)
    result = result.where(result.notnull(), None)

    return result.to_dict(orient="records")
@app.post("/cross-database-query")
def cross_database_query(request: ChatRequest):

    result = run_cross_database_query(request.question)

    result = result.astype(object)
    result = result.where(result.notna(), None)

    return {
        "question": request.question,
        "rows": len(result),
        "result": result.to_dict(orient="records")
    }