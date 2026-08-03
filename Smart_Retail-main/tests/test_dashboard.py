"""Unit tests for Dashboard Stats API endpoint."""

def test_dashboard_stats_unauthorized(client):
    """Test dashboard stats without API key returns 401."""
    response = client.get("/dashboard/stats")
    assert response.status_code == 401


def test_dashboard_stats_success(client, auth_headers):
    """Test retrieving consolidated dashboard stats."""
    response = client.get("/dashboard/stats", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_customers" in data
    assert "total_visits" in data
    assert "total_reviews" in data
    assert "total_chat_queries" in data
    assert "sentiment_breakdown" in data
    assert "recent_visits" in data
    assert data["system_status"] == "Operational"
