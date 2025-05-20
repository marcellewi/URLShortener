from fastapi import status


def test_root_endpoint(client):
    """Test the root endpoint returns the welcome message"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to the URL Shortener application"}


def test_create_short_url(client):
    """Test creating a shortened URL"""
    payload = {"original_url": "https://example.com", "custom_alias": None}
    response = client.post("/api/urls/shorten", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["original_url"] == "https://example.com/"
    assert data["short_code"] is not None
    assert data["short_url"].endswith(data["short_code"])
    assert data["is_custom"] is False


def test_get_short_url(client):
    """Test retrieving a short URL"""
    payload = {"original_url": "https://example.org", "custom_alias": None}
    create_response = client.post("/api/urls/shorten", json=payload)
    short_code = create_response.json()["short_code"]

    response = client.get(f"/api/urls/{short_code}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["original_url"] == "https://example.org/"
    assert data["short_code"] == short_code


def test_custom_alias(client):
    """Test creating a URL with a custom alias"""
    payload = {"original_url": "https://example.net", "custom_alias": "my_custom_alias"}
    response = client.post("/api/urls/shorten", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["original_url"] == "https://example.net/"
    assert data["short_code"] == "my_custom_alias"
    assert data["is_custom"] is True
