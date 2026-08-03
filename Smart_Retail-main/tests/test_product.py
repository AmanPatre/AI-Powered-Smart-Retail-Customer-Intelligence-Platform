"""Unit tests for Product Image Classification API endpoint."""

def test_product_classification_unauthorized(client, sample_image_bytes):
    """Test request without API key returns 401 Unauthorized."""
    response = client.post(
        "/classify-product",
        files={"file": ("product.jpg", sample_image_bytes, "image/jpeg")},
    )
    assert response.status_code == 401


def test_product_classification_success(client, auth_headers, sample_image_bytes):
    """Test product classification request with valid image and API key."""
    response = client.post(
        "/classify-product",
        headers=auth_headers,
        files={"file": ("product.jpg", sample_image_bytes, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert "confidence" in data
    assert "probabilities" in data
    assert isinstance(data["probabilities"], dict)
    assert data["category"] in ["Apparel", "Electronics", "Footwear", "Groceries", "Home Goods"]
