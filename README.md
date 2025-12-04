# 🧠 DocuBot – Your Documentation Retrieval Assistant

DocuBot is a lightweight simulation of a RAG (Retrieval-Augmented Generation) system.  
Your task is to improve the retrieval and response logic so DocuBot becomes a helpful assistant for developers.

## What You Can Do

- Inspect how DocuBot loads and searches files.
- Improve the retrieval algorithm (scoring, ranking, chunking).
- Add guardrails and better formatting to the output.
- Test DocuBot on your own project documentation.

## How to Run

```bash
python main.py
```

DocuBot will search the `docs/` folder for `.txt`, `.md`, and `.py` files.

## Suggested Improvements

- Add keyword scoring or weighting.
- Implement snippet chunking for long documents.
- Add source citations or confidence scores.
- Build simple evaluation tests for correctness and relevance.
- Add AI summarization (optional extension).
