from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.database.database import SessionLocal
from backend.database.models import Document, DocumentChunk
from backend.services.document_processor import extract_text_from_pdf
from rag.chunker import split_text_into_chunks


router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path("data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    if file.content_type not in (None, "application/pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid content type. Upload a PDF file.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB.",
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF.",
        )

    file_path = UPLOAD_DIR / f"{uuid4().hex}.pdf"

    try:
        # 1. Save the PDF
        file_path.write_bytes(content)

        # 2. Extract text
        extracted_text = extract_text_from_pdf(str(file_path))

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text found in PDF. "
                    "Scanned PDFs require OCR."
                ),
            )

        # 3. Split extracted text into chunks
        chunks = split_text_into_chunks(extracted_text)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Could not create text chunks from this PDF.",
            )

        # 4. Create the document record
        document = Document(
            filename=Path(file.filename).name,
            file_path=str(file_path),
            status="processed",
            extracted_text=extracted_text,
        )

        db.add(document)
        db.flush()  # Generate document.id without committing yet

        # 5. Save each chunk linked to its document
        for index, chunk_text in enumerate(chunks):
            db.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk_text,
                )
            )

        # 6. Commit document and chunks together
        db.commit()
        db.refresh(document)

        return {
            "message": "PDF processed and chunks saved successfully",
            "document_id": document.id,
            "filename": document.filename,
            "status": document.status,
            "characters_extracted": len(extracted_text),
            "chunks_created": len(chunks),
            "preview": extracted_text[:300],
        }

    except HTTPException:
        db.rollback()
        file_path.unlink(missing_ok=True)
        raise

    except Exception:
        db.rollback()
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail="Could not process the PDF and save its chunks.",
        )

    finally:
        await file.close()


@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(Document.id.desc()).all()

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "status": document.status,
            "created_at": document.created_at,
        }
        for document in documents
    ]


@router.get("/{document_id}/chunks")
def list_document_chunks(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index)
        .all()
    )

    return {
        "document_id": document_id,
        "total_chunks": len(chunks),
        "chunks": [
            {
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
            }
            for chunk in chunks
        ],
    }
