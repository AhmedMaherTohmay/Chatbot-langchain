import pytest
from tools import VectorStoreRetriever, generate_embedding

# Fixture for sample documents
@pytest.fixture
def sample_docs():
    return [
        {"page_content": "This is a document about the app."},
        {"page_content": "This is another document about policies."},
        {"page_content": "This document is unrelated."},
    ]

# Fixture for the retriever
@pytest.fixture
def retriever(sample_docs):
    return VectorStoreRetriever.from_docs(sample_docs)

def test_generate_embedding():
    """Test if embeddings are generated correctly."""
    text = "This is a test."
    embedding = generate_embedding(text)
    assert isinstance(embedding, list)
    assert len(embedding) > 0

def test_retriever_query(retriever):
    """Test if the retriever returns the correct documents."""
    query = "Tell me about the app"
    results = retriever.query(query, k=2)
    assert len(results) == 2
    assert "app" in results[0]["page_content"]

def test_retriever_empty_docs():
    """Test the retriever with no documents."""
    retriever = VectorStoreRetriever.from_docs([])
    results = retriever.query("test query", k=2)
    assert len(results) == 0

def test_retriever_k_larger_than_docs(retriever):
    """Test if k is adjusted when it exceeds the number of documents."""
    results = retriever.query("test query", k=10)
    assert len(results) == 3  # Only 3 documents exist