"""Unit tests for Sentiment Analysis API endpoint."""

def test_sentiment_analysis_unauthorized(client):
    """Test sentiment request without API key returns 401."""
    response = client.post(
        "/analyze-sentiment",
        json={"review_text": "Great store experience!"},
    )
    assert response.status_code == 401


def test_sentiment_analysis_positive(client, auth_headers):
    """Test sentiment analysis for positive review text."""
    payload = {"review_text": "Superb store quality and very friendly staff!"}
    response = client.post(
        "/analyze-sentiment",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "Positive"
    assert data["confidence"] > 0.4
    assert "review_id" in data


def test_sentiment_analysis_negative(client, auth_headers):
    """Test sentiment analysis for negative review text."""
    payload = {"review_text": "Terrible customer service, rude cashiers and broken item."}
    response = client.post(
        "/analyze-sentiment",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "Negative"
