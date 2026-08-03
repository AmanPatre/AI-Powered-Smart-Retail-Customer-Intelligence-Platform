"""Unit tests for Retail FAQ Chatbot API endpoint."""

def test_chatbot_unauthorized(client):
    """Test chatbot request without API key returns 401."""
    response = client.post(
        "/chatbot",
        json={"message": "What are your store hours?"},
    )
    assert response.status_code == 401


def test_chatbot_store_hours(client, auth_headers):
    """Test chatbot query regarding store opening hours."""
    payload = {"message": "What time do you open and close?"}
    response = client.post(
        "/chatbot",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "store_hours"
    assert "response" in data
    assert data["confidence"] > 0.3


def test_chatbot_return_policy(client, auth_headers):
    """Test chatbot query regarding return policy."""
    payload = {"message": "What is your return policy?"}
    response = client.post(
        "/chatbot",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "return_policy"
