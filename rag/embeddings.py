from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

# Load the embedding model once
model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts: list[str]):
    """
    Convert a list of text chunks into numerical vectors.
    """

    if not texts:
        return []

    if any(not text.strip() for text in texts):
        raise ValueError("Texts must not contain empty strings.")

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    return embeddings
