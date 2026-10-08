from rag.chunker import split_text_into_chunks


sample_text = """
Financial compliance requires accurate records.

Organizations should maintain proper documentation.
Transactions must be reviewed regularly.

Suspicious activities should be reported according
to applicable rules and regulations.
"""

chunks = split_text_into_chunks(sample_text)

print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk)
    print("Characters:", len(chunk))
    
