import os
import secrets


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))
    JWT_EXPIRY_MINUTES = 15
    BCRYPT_ROUNDS = 10
    MAX_LOGIN_ATTEMPTS = 5
    RATE_LIMIT_WINDOW_SECONDS = 60
    RATE_LIMIT_MAX_REQUESTS = 5
