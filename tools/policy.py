import re
import requests
import numpy as np
from langchain_core.tools import tool
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
# Retrieve the API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
# Pass it to the configure method
genai.configure(api_key=gemini_api_key)


# Function to generate embeddings using Google's Text Embedding 004
def generate_embedding(text: str) -> list[float]:
    """Generate embeddings for a given text using Google's Text Embedding 004."""
    response = genai.embed_content(model="models/text-embedding-004", content=text)
    return response["embedding"]

# Fetching the FAQ content
response = requests.get(
    "https://drive.usercontent.google.com/u/0/uc?id=1QTtXkjUUgNBBdjGczP1pj94O1U11hTB6&export=download"
)
response.raise_for_status()
faq_text = response.text

# Split the FAQ into individual documents
docs = [{"page_content": txt} for txt in re.split(r"(?=\n##)", faq_text)]

class VectorStoreRetriever:
    def __init__(self, docs: list, vectors: np.ndarray):
        self._arr = np.array(vectors)
        self._docs = docs

    @classmethod
    def from_docs(cls, docs):
        # Generate embeddings using Google's Text Embedding 004
        embeddings = [generate_embedding(doc["page_content"]) for doc in docs]
        vectors = np.array(embeddings, dtype="float32")
        return cls(docs, vectors)

    def query(self, query: str, k: int = 5) -> list[dict]:
        # Generate embedding for the query
        query_vector = np.array(generate_embedding(query), dtype="float32")
        # Compute cosine similarity using matrix multiplication
        scores = query_vector @ self._arr.T
        # Ensure k does not exceed the number of documents
        k = min(k, len(self._docs))
        if k == 0:
            return []  # Return an empty list if there are no documents
        # Get the top-k most similar documents
        top_k_idx = np.argpartition(scores, -k)[-k:]
        top_k_idx_sorted = top_k_idx[np.argsort(-scores[top_k_idx])]
        return [
            {**self._docs[idx], "similarity": scores[idx]} for idx in top_k_idx_sorted
        ]

# Initialize the retriever
retriever = VectorStoreRetriever.from_docs(docs)
@tool
def lookup_policy(query: str) -> str:
    """Consult the company policies to check whether certain options are permitted.
    Use this before making any flight changes or performing other 'write' events."""
    docs = retriever.query(query, k=2)
    if not docs:
        return "I couldn't find any relevant information. Please contact our support team for further assistance."
    return "\n\n".join([doc["page_content"] for doc in docs])

if __name__ == "__main__":
    print(lookup_policy("what is the app name"))