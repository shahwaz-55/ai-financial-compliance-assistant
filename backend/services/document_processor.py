import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """Extract readable text from a PDF file."""
    extracted_pages = []

    with fitz.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text").strip()

            if page_text:
                extracted_pages.append(
                    f"[Page {page_number}]\n{page_text}"
                )

    return "\n\n".join(extracted_pages)
