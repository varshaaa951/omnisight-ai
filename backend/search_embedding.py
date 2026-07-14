import psycopg2
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
FROM ai_schema_embeddings
ORDER BY embedding <=> %s::vector
LIMIT 3;
""", (query_embedding,))

results = cur.fetchall()

context = "Relevant Database Schema\n\n"

for row in results:
    context += row[0] + "\n\n"

print(context)

cur.close()
conn.close()