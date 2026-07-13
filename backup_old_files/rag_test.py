import psycopg2
import ollama
from sentence_transformers import SentenceTransformer

conn = psycopg2.connect(
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

question = "How many customers do we have?"

query_embedding = model.encode(question).tolist()

cur = conn.cursor()

cur.execute("""
SELECT content
FROM company_knowledge
ORDER BY embedding <=> %s::vector
LIMIT 1;
""", (query_embedding,))

knowledge = cur.fetchone()[0]

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

print(response["message"]["content"])

cur.close()
conn.close()