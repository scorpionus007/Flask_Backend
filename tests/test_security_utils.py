def test_password_hashing_and_verification():
    from app.utils.security import hash_password, verify_password

    password = "StrongPass123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
