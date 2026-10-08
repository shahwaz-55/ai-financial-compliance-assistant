import faiss
import numpy as np

from rag.embeddings import generate_embeddings


def build_vector_index(texts: list[str]):
    """
    Create a FAISS index from text chunks.
    Returns the index and the original texts.
    """

    if not texts:
        raise ValueError("At least one text chunk is required.")

    embeddings = generate_embeddings(texts)
    embeddings = np.asarray(embeddings, dtype=np.float32)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index, texts


def search_similar_chunks(
    query: str,
    index,
    texts: list[str],
    top_k: int = 3,
):
    """
    Retrieve the most similar text chunks for a query.
    """

    if not query.strip():
        raise ValueError("Query must not be empty.")

    if index.ntotal == 0 or not texts:
        return []

    query_embedding = generate_embeddings([query])
    query_embedding = np.asarray(
        query_embedding,
        dtype=np.float32,
    )

    k = min(top_k, index.ntotal)

    scores, indices = index.search(query_embedding, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        results.append(
            {
                "text": texts[int(idx)],
                "score": float(score),
            }
        )

    return results
