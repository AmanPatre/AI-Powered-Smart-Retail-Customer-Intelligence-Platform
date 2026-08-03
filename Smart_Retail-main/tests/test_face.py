"""Unit tests for Face Recognition API endpoint."""

def test_face_recognition_unauthorized(client, sample_image_bytes):
    """Test request without API key returns 401 Unauthorized."""
    response = client.post(
        "/recognize-face",
        files={"file": ("test.jpg", sample_image_bytes, "image/jpeg")},
    )
    assert response.status_code == 401


def test_face_recognition_success(client, auth_headers, sample_image_bytes):
    """Test face recognition request with valid image and API key."""
    response = client.post(
        "/recognize-face",
        headers=auth_headers,
        files={"file": ("test_face.jpg", sample_image_bytes, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "recognized" in data
    assert "confidence" in data
    assert "faces_detected" in data
    assert isinstance(data["faces_detected"], int)
