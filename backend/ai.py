import ollama
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- General LLM ----------
def ask_llm(prompt):

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# ---------- Text-to-SQL Prompt ----------
SQL_SYSTEM_PROMPT = """
You are an expert PostgreSQL database analyst.

Your responsibilities:

- Read the supplied database schema context carefully.
- Understand the user's question.
- Use ONLY the supplied tables and columns.
- Generate ONE valid PostgreSQL SQL query.
- Return ONLY executable SQL.
- Do NOT explain your answer.
- Do NOT use markdown.
- Do NOT include ```sql.
- Do NOT include comments.
- Output exactly one SQL statement.
"""


# ---------- Text-to-SQL Function ----------
def generate_sql(question, schema_context):

    prompt = f"""
Database Schema:

{schema_context}

User Question:

{question}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": SQL_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()