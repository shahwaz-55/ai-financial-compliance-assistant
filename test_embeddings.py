
from rag.embeddings import generate_embeddings


sample_chunks = [
    "Financial compliance requires accurate records.",
    "Organizations must maintain financial documents.",
    "The weather is pleasant today.",
]

embeddings = generate_embeddings(sample_chunks)

print("Number of text chunks:", len(sample_chunks))
print("Embeddings shape:", embeddings.shape)
print("First embedding dimensions:", len(embeddings[0]))
print("First 5 values:", embeddings[0][:5])
