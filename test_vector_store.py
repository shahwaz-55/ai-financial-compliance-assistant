from rag.vector_store import (
    build_vector_index,
    search_similar_chunks,
)


sample_chunks = [
    "Financial compliance requires accurate records and documentation.",
    "Organizations must review financial transactions regularly.",
    "The weather is pleasant and sunny today.",
]

index, stored_texts = build_vector_index(sample_chunks)

print("Total vectors stored:", index.ntotal)

query = "How should financial transactions be checked?"

results = search_similar_chunks(
    query=query,
    index=index,
    texts=stored_texts,
    top_k=2,
)

print("\nQuery:", query)
print("\nMost relevant chunks:")

for result in results:
    print("\nScore:", round(result["score"], 4))
    print("Text:", result["text"])
