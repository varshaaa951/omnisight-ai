from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "OmniSight AI currently has 500 customers."

embedding = model.encode(text)

print("Vector Length:", len(embedding))
print(embedding[:10])