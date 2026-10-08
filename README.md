# AI Financial Compliance Assistant

An AI-powered financial compliance assistant built with:

- Next.js + Tailwind CSS
- Python + FastAPI
- Gemini / OpenAI API
- LangChain
- Sentence Transformers
- FAISS
- PostgreSQL
- Scikit-learn
- PyTest
- Postman
- GitHub Actions
- Vercel + Render/Railway

## Project Goal

Upload financial/compliance documents, retrieve relevant information with RAG, generate grounded AI answers with citations, and provide compliance/risk analysis.

## Current Status

Initial project scaffold created. Implementation will be completed step by step.

## Local Backend

Create and activate a Python virtual environment, install `requirements.txt`, then run:

```bash
uvicorn backend.main:app --reload
```

API:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## Frontend

The Next.js application will be initialized in the `frontend/` directory in the next implementation step.
