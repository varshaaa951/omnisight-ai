import psycopg2
from sentence_transformers import SentenceTransformer

conn = psycopg2.connect(
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "OmniSight AI currently has 500 customers."

embedding = model.encode(text).tolist()

cur = conn.cursor()

cur.execute(
    """
    INSERT INTO company_knowledge (content, embedding)
    VALUES (%s, %s)
    """,
    (text, embedding)
)

conn.commit()

cur.close()
conn.close()

print("Embedding stored successfully!")