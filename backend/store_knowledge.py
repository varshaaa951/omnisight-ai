from database import get_connection, return_connection
from ai import model

knowledge = [
    "OmniSight AI is an intelligent business assistant that helps organizations analyze customers, orders, and revenue using artificial intelligence.",

    "The system uses PostgreSQL with pgvector to store vector embeddings for Retrieval Augmented Generation.",

    "OmniSight AI uses Ollama running the Llama 3.2 model for local AI inference.",

    "Users can ask business questions in natural language and receive AI-generated insights."
]

conn = get_connection()
cur = conn.cursor()

for text in knowledge:

    embedding = model.encode(text).tolist()

    cur.execute(
        """
        INSERT INTO company_knowledge(content, embedding)
        VALUES (%s, %s::vector)
        """,
        (text, embedding)
    )

conn.commit()

cur.close()
return_connection(conn)

print("Knowledge stored successfully!")