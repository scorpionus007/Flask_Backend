def test_auth_register_endpoint_exists():
    from app.main import create_app
    app = create_app()
    client = app.test_client()

    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "Test@1234"
    })

    # We don’t care if it succeeds or fails,
    # we onlycare that the oute exist and responds
    assert response.status_code in [200, 201, 400]
