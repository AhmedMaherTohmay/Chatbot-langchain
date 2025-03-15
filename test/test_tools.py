import pytest
from tools import VectorStoreRetriever, generate_embedding, lookup_policy

# Fixture for sample documents
@pytest.fixture
def sample_docs():
    return [
        {"page_content": "Policy 1: Each passenger can carry two bags."},
        {"page_content": "Policy 2: No pets allowed on flights."},
    ]

# Fixture for the retriever
@pytest.fixture
def retriever(sample_docs):
    return VectorStoreRetriever.from_docs(sample_docs)

def test_lookup_policy(retriever):
    """Test if the lookup_policy tool returns the correct policy."""
    query = "What is the baggage policy?"
    result = lookup_policy(query)
    assert "bags" in result

def test_lookup_policy_no_results(retriever):
    """Test the lookup_policy tool with no matching documents."""
    query = "What is the refund policy?"
    result = lookup_policy(query)
    assert "I couldn't find any relevant information" in result