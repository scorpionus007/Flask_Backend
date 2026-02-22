from app.extensions import users_db
from app.config import Config
from app.utils.security import hash_password, verify_password, generate_jwt
from app.utils.logger import audit_logger


def register_user(username: str, password: str, role: str = "user") -> dict:
    if username in users_db:
        return {"error": "Username already exists", "status": 409}

    if len(password) < 8:
        return {"error": "Password must be at least 8 characters", "status": 400}

    users_db[username] = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "failed_attempts": 0,
        "locked": False,
    }
    return {"message": "User registered successfully", "status": 201}


def authenticate_user(username: str, password: str, client_ip: str) -> dict:
    user = users_db.get(username)

    if not user:
        return {"error": "Invalid credentials", "status": 401}

    if user["locked"]:
        audit_logger.warning(
            "Login attempt on locked account | ip=%s | user=%s",
            client_ip,
            username,
        )
        return {"error": "Account is locked", "status": 403}

    if not verify_password(password, user["password_hash"]):
        user["failed_attempts"] += 1
        audit_logger.warning(
            "Failed login attempt | ip=%s | user=%s | attempts=%d",
            client_ip,
            username,
            user["failed_attempts"],
        )
        if user["failed_attempts"] >= Config.MAX_LOGIN_ATTEMPTS:
            user["locked"] = True
            audit_logger.critical(
                "Account locked | ip=%s | user=%s", client_ip, username
            )
        return {"error": "Invalid credentials", "status": 401}

    user["failed_attempts"] = 0
    token = generate_jwt(username, user["role"])
    audit_logger.info("Successful login | ip=%s | user=%s", client_ip, username)
    return {"token": token, "status": 200}
