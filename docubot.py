# Core DocuBot logic – a lightweight retrieval assistant.

import os

class DocuBot:
    def __init__(self, folder_path="docs"):
        self.folder_path = folder_path
        self.documents = self.load_documents()

    def load_documents(self):
        """Load .txt, .md, or .py files from the docs folder."""
        docs = []
        if not os.path.exists(self.folder_path):
            print(f"Folder '{self.folder_path}' not found.")
            return docs
        
        for file in os.listdir(self.folder_path):
            if file.endswith((".txt", ".md", ".py")):
                with open(os.path.join(self.folder_path, file), "r", encoding="utf-8") as f:
                    docs.append((file, f.read()))
        return docs

    def retrieve(self, query):
        """Retrieve relevant snippets based on a keyword match.
        TODO: Improve this retrieval logic (e.g., score by frequency, chunk text, partial match)."""
        results = []
        for filename, text in self.documents:
            if query.lower() in text.lower():
                snippet = text[:500]  # basic preview
                results.append((filename, snippet))
        return results

    def assemble_answer(self, query, snippets):
        """Build a response from retrieved context.
        TODO: Improve formatting, add citations, add fallback if no results."""
        if not snippets:
            return f"No relevant documentation found for '{query}'."

        output = [f"### Results for: '{query}'\n"]
        for filename, snippet in snippets:
            output.append(f"From **{filename}**:\n{snippet}\n")
        return "\n".join(output)
