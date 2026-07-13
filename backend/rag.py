from database import get_connection, return_connection
from ai import model, ask_llm


def rag_answer(question):

    query_embedding = model.encode(question).tolist()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT content
        FROM company_knowledge
        ORDER BY embedding <=> %s::vector
        LIMIT 1;
    """, (query_embedding,))

    result = cur.fetchone()

    return_connection(conn)

    if result is None:
        return "No company knowledge found."

    knowledge = result[0]

    prompt = f"""
You are OmniSight AI.

Use ONLY the following company knowledge to answer the question.

Company Knowledge:
{knowledge}

Question:
{question}

Answer professionally.
"""

    answer = ask_llm(prompt)

    return answer
