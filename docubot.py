"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
- Supporting retrieval only answers
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

import os
import glob
import string

class DocuBot:
    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents into memory
        self.documents = self.load_documents()  # List of (filename, text)

        # Identify smaller chunks of documents
        self.chunks = self.chunk_documents(self.documents)

        # Build a retrieval index (implemented in Phase 1)
        self.index = self.build_index(self.documents)

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                docs.append((filename, text))
        return docs

    # -----------------------------------------------------------
    # Index Construction (Phase 1)
    # -----------------------------------------------------------

    def chunk_documents(self, documents):
        """
        Splits each document into sections based on markdown headers.
        Returns a list of (filename, heading, text) tuples.
        """
        chunks = []
        for filename, text in documents:
            lines = text.split("\n")
            current_heading = "(intro)"
            current_lines = []

            for line in lines:
                if line.startswith("#"):
                    section_text = "\n".join(current_lines).strip()
                    if section_text:
                        chunks.append((filename, current_heading, section_text))
                    current_heading = line.lstrip("#").strip()
                    current_lines = [line]
                else:
                    current_lines.append(line)
                
            # Flush the last section
            section_text = "\n".join(current_lines).strip()
            if section_text:
                chunks.append((filename, current_heading, section_text))

        return chunks

    def build_index(self, documents):
        """
        (Phase 1):
        Build a tiny inverted index mapping lowercase words to the documents
        they appear in.

        Example structure:
        {
            "token": ["AUTH.md", "API_REFERENCE.md"],
            "database": ["DATABASE.md"]
        }

        Keep this simple: split on whitespace, lowercase tokens,
        ignore punctuation if needed.
        """
        index = {}
        for filename, text in documents:
            for word in text.split():
                token = word.lower().strip(".,:#`\"'()-[]{}*/\\")
                if token and filename not in index.get(token, []):
                    index.setdefault(token, []).append(filename)
        return index

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1)
    # -----------------------------------------------------------

    def _stem(self, word):
        for suffix in ("ation", "tion", "ing", "ed", "ion"):
            if len(word) > len(suffix) + 3 and word.endswith(suffix):
                return word[:-len(suffix)]
        return word

    def score_document(self, query, text):
        """
        (Phase 1):
        Return a simple relevance score for how well the text matches the query.

        Suggested baseline:
        - Convert query into lowercase words
        - Count how many appear in the text
        - Return the count as the score
        """
        STOP_WORDS = {"are", "is", "the", "a", "an", "in", "of", "to", "do", "i",
              "how", "what", "why", "when", "where", "does", "can", "will"}
        
        query_words = [
            self._stem(w.strip(string.punctuation))
            for w in query.lower().split()
            if w.strip(string.punctuation) not in STOP_WORDS]
        text_words = set()
        for w in text.lower().split():
            parts = w.strip(string.punctuation).replace("_", " ").split()
            text_words.update(self._stem(p) for p in parts)
        return sum(1 for word in query_words if word in text_words)

    def retrieve(self, query, top_k=3, min_score=1):
        """
        (Phase 1):
        Use the index and scoring function to select top_k relevant document snippets.

        Return a list of (filename, text) sorted by score descending.
        """
        results = []
        for filename, heading, text in self.chunks:
            score = self.score_document(query, heading + " " + text)
            if score >= min_score:
                results.append((filename, heading, text, score))
        
        results.sort(key=lambda x: x[3], reverse=True)
        return [(filename, heading, text) for filename, heading, text, _ in results[:top_k]]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, heading, text in snippets:
            formatted.append(f"[{filename} - {heading}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        This is used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
