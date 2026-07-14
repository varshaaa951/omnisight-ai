from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

from database import get_connection, return_connection
from schema_catalog import extract_schema

model = SentenceTransformer("all-MiniLM-L6-v2")

# Central vector catalog is stored in omnisight
conn = get_connection("omnisight")
register_vector(conn)

cur = conn.cursor()

databases = [
    ("omnisight", "omnisight"),
    ("marketing_db", "marketing_db")
]

for db_name, source in databases:

    schema = extract_schema(db_name)

    for table in schema:

        text = f"Table {table}. "

        for col in schema[table]:
            text += f"{col['column']} is {col['type']}. "

        embedding = model.encode(text).tolist()

        cur.execute(
            """
            INSERT INTO ai_schema_embeddings
            (content, embedding, source)
            VALUES (%s, %s, %s)
            """,
            (text, embedding, source)
        )

conn.commit()

cur.close()
return_connection(conn, "omnisight")

print("✅ All schema embeddings stored successfully.")