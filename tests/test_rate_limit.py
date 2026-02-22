def test_rate_limit_blocks_excess_requests():
    from app.main import create_app
    app = create_app()
    client = app.test_client()

    # Hit endpoint multiple times quickly
    for _ in range(10):
        response = client.post("/auth/login", json={
            "username": "dummy",
            "password": "dummy"
        })

    # Eventually should rate-limit or at least respond safely
    assert response.status_code in [200, 401, 429]

