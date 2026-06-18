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
FROM company_knowledge
ORDER BY embedding <=> %s::vector
LIMIT 1;
""", (query_embedding,))

result = cur.fetchone()

print("Most Relevant Knowledge:")
print(result[0])

cur.close()
conn.close()