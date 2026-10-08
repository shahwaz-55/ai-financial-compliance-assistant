
from sqlalchemy.orm import Session

from backend.database.models import Document, DocumentChunk
from rag.vector_store import (
    build_vector_index,
    search_similar_chunks,
)


def retrieve_relevant_chunks(
    db: Session,
    query: str,
    top_k: int = 3,
    document_id: int | None = None,
):
    """
    Retrieve relevant text chunks from uploaded PDF documents.
    """

    if not query or not query.strip():
        raise ValueError("Query must not be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    # Fetch chunks belonging to processed documents.
    db_query = (
        db.query(DocumentChunk)
        .join(
            Document,
            Document.id == DocumentChunk.document_id,
        )
        .filter(Document.status == "processed")
    )

    # Optionally search within one specific document.
    if document_id is not None:
        document = db.get(Document, document_id)

        if document is None:
            raise LookupError("Document not found.")

        db_query = db_query.filter(
            DocumentChunk.document_id == document_id
        )

    chunks = db_query.order_by(
        DocumentChunk.document_id,
        DocumentChunk.chunk_index,
    ).all()

    if not chunks:
        return []

    # Extract text and build a temporary FAISS index.
    chunk_texts = [chunk.content for chunk in chunks]

    index, stored_texts = build_vector_index(chunk_texts)

    # Search for the most relevant chunks.
    results = search_similar_chunks(
        query=query,
        index=index,
        texts=stored_texts,
        top_k=top_k,
    )

    # Attach database information to each result.
    text_to_chunks = {}

    for chunk in chunks:
        text_to_chunks.setdefault(chunk.content, []).append(chunk)

    enriched_results = []

    for result in results:
        matching_chunks = text_to_chunks.get(result["text"], [])

        if not matching_chunks:
            continue

        chunk = matching_chunks.pop(0)
        document = db.get(Document, chunk.document_id)

        enriched_results.append(
            {
                "document_id": chunk.document_id,
                "filename": document.filename if document else None,
                "chunk_index": chunk.chunk_index,
                "score": result["score"],
                "content": chunk.content,
            }
        )

    return enriched_results
