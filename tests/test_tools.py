import pytest
from tools import VectorStoreRetriever, generate_embedding, App_Details, search_transactions

# Fixture for sample documents
@pytest.fixture
def sample_docs():
    return [
        {"page_content": "Policy 1: Each transaction is charged a fee of 2%."},
        {"page_content": "Policy 2: Refunds are processed within 5 business days."},
        {"page_content": "Policy 3: The PayNow app supports instant payments."},
    ]

# Fixture for the retriever
@pytest.fixture
def retriever(sample_docs):
    return VectorStoreRetriever.from_docs(sample_docs)

def test_lookup_policy_transaction_fee(retriever):
    """Test if the lookup_policy tool returns the correct transaction fee policy."""
    query = "What is the transaction fee?"
    result = App_Details(query)
    assert "2%" in result

def test_lookup_policy_refund_policy(retriever):
    """Test if the lookup_policy tool returns the correct refund policy."""
    query = "How long does a refund take?"
    result = App_Details(query)
    assert "5 business days" in result

def test_lookup_policy_app_support(retriever):
    """Test if the lookup_policy tool returns information about the PayNow app."""
    query = "Does PayNow support instant payments?"
    result = App_Details(query)
    assert "instant payments" in result

def test_lookup_policy_no_results(retriever):
    """Test the lookup_policy tool with no matching documents."""
    query = "What is the cancellation policy?"
    result = App_Details(query)
    assert "I couldn't find any relevant information" in result

def test_search_transactions():
    """Test if the search_transactions tool returns the correct transaction link."""
    transaction_type = "video"
    result = search_transactions(transaction_type)
    assert "https://www.youtube.com" in result

def test_search_transactions_invalid_type():
    """Test the search_transactions tool with an invalid transaction type."""
    transaction_type = "invalid"
    result = search_transactions(transaction_type)
    assert "Transaction type not found" in result