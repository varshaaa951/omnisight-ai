from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

from database import get_connection, return_connection
from schema_catalog import extract_schema

model = SentenceTransformer("all-MiniLM-L6-v2")

conn = get_connection()
register_vector(conn)

cur = conn.cursor()

schema = extract_schema()

for table in schema:

    text = f"Table {table}. "

    for col in schema[table]:

        text += f"{col['column']} is {col['type']}. "

    embedding = model.encode(text).tolist()

    cur.execute(
        """
        INSERT INTO ai_schema_embeddings(content, embedding)
        VALUES (%s,%s)
        """,
        (text, embedding)
    )

conn.commit()

cur.close()
return_connection(conn)

print("✅ Schema embeddings stored successfully.")