from backend.database.database import SessionLocal
from backend.services.retrieval_service import retrieve_relevant_chunks


if __name__ == "__main__":
    query = input("Enter your question about uploaded PDFs: ").strip()

    with SessionLocal() as db:
        try:
            results = retrieve_relevant_chunks(
                db=db,
                query=query,
                top_k=3,
            )

            if not results:
                print("\nNo document chunks found in the database.")
            else:
                print(f"\nRelevant chunks found: {len(results)}")

                for number, result in enumerate(results, start=1):
                    print(f"\n--- Result {number} ---")
                    print("Document ID:", result["document_id"])
                    print("Filename:", result["filename"])
                    print("Chunk index:", result["chunk_index"])
                    print("Similarity score:", round(result["score"], 4))
                    print("Content:")
                    print(result["content"])

        except Exception as error:
            print(f"\nRetrieval failed: {error}")
            raise
