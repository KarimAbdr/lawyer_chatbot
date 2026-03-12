# MVP Czech Legal AI Assistant
<img width="1466" height="850" alt="Screenshot 2026-03-12 at 20 29 05" src="https://github.com/user-attachments/assets/1de4dee9-bc80-42f1-882f-30ce9289af91" />


<img width="1450" height="843" alt="Screenshot 2026-03-12 at 20 31 59" src="https://github.com/user-attachments/assets/34e1cef5-3f60-450c-a77e-0c6e8d5918b7" />

A chatbot that answers questions about Czech business law using RAG (Retrieval-Augmented Generation). It reads actual legal text, finds the relevant sections, and gives you an answer with citations.

Currently covers two laws:
- **Business Corporations Act** (90/2012) — company formation, s.r.o., a.s., cooperatives
- **Trade Licensing Act** (455/1991) — trade licences, conditions, permits

## How It Works

You ask a question in plain English. The system finds the most relevant legal sections from the database, feeds them to an LLM (Gemini), and the LLM writes an answer based only on those sections. Every answer includes source citations so you can verify it.

```
Question → Embed → Search ChromaDB → Top 5 sections → Gemini → Answer + Sources
```

## Tech Stack

- **FastAPI** — backend
- **ChromaDB** — vector database
- **sentence-transformers** — text embeddings (all-MiniLM-L6-v2)
- **Google Gemini** — answer generation
- **Vanilla JS** — frontend (no framework needed)

## Data Pipeline

The legal texts go through this process before the chatbot can use them:

1. **PDF → Markdown** using Docling
2. **Markdown → JSON** using a custom state-machine parser
3. **JSON → ChromaDB** using sentence-transformers for embeddings

Each section becomes one chunk with metadata (law name, chapter, section number) so the chatbot can cite its sources.

## Smart Retrieval

Basic search sometimes misses relevant sections. Smart retrieval fixes this by:

1. Searching with the full question
2. Extracting key phrases and searching for each separately
3. Merging all results and removing duplicates

This catches sections that basic vector search would miss.
