import psycopg2
from sentence_transformers import SentenceTransformer

conn = psycopg2.connect(
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

cur = conn.cursor()

cur.execute("""
SELECT id, content
FROM company_knowledge
WHERE embedding IS NULL
""")

rows = cur.fetchall()

for row in rows:
    id = row[0]
    content = row[1]

    embedding = model.encode(content).tolist()

    cur.execute(
        """
        UPDATE company_knowledge
        SET embedding = %s
        WHERE id = %s
        """,
        (embedding, id)
    )

    print(f"Updated row {id}")

conn.commit()

cur.close()
conn.close()

print("All embeddings updated!")