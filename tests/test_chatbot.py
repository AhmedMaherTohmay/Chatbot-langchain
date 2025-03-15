from chat import llm_response
def test_chatbot_workflow():
    """Test the chatbot workflow for a payment-related query."""
    query = "What is the transaction fee?"
    response = llm_response(query)
    assert "2%" in response