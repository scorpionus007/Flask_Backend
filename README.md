# Secure Flask Backend

A production-grade, security-focused Flask API demonstrating authentication, RBAC, rate limiting, account lockout, audit logging, and centralized error handling.

## Tech Stack

- Python 3.10+
- Flask
- PyJWT
- bcrypt
- In-memory storage

## Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd secure_backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app/main.py
```

The server starts on `http://0.0.0.0:5000`.

## API Endpoints

| Method | Endpoint           | Description          | Auth Required |
|--------|--------------------|----------------------|---------------|
| POST   | `/auth/register`   | Register a new user  | No            |
| POST   | `/auth/login`      | Login and get JWT    | No            |
| GET    | `/auth/protected`  | Authenticated route  | Bearer Token  |
| GET    | `/admin/dashboard` | Admin-only route     | Bearer Token (admin role) |

## Usage Examples

### Register a User
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepass123"}'
```

### Register an Admin
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "adminpass123", "role": "admin"}'
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepass123"}'
```

### Access Protected Route
```bash
curl http://localhost:5000/auth/protected \
  -H "Authorization: Bearer <token>"
```

### Access Admin Dashboard
```bash
curl http://localhost:5000/admin/dashboard \
  -H "Authorization: Bearer <token>"
```

## Security Features

- **JWT Authentication** — 15-minute token expiry, HS256 signing
- **Password Hashing** — bcrypt with 10 salt rounds
- **Rate Limiting** — 5 login attempts per minute per IP
- **Account Lockout** — Account locked after 5 consecutive failed logins
- **RBAC** — Role-based access control via middleware decorators
- **Audit Logging** — All security events logged with timestamp and IP
- **Error Handling** — Centralized JSON error responses, no stack trace leakage

## Project Structure

```
secure_backend/
├── app/
│   ├── main.py              # Application entry point & factory
│   ├── config.py            # Centralized configuration
│   ├── extensions.py        # In-memory data stores
│   ├── __init__.py
│   ├── middleware/
│   │   ├── auth.py          # JWT & RBAC decorators
│   │   └── rate_limit.py    # IP-based rate limiter
│   ├── routes/
│   │   ├── auth.py          # Auth endpoints
│   │   └── admin.py         # Admin endpoints
│   ├── services/
│   │   └── user_service.py  # Business logic
│   └── utils/
│       ├── security.py      # Crypto utilities
│       ├── logger.py        # Audit logger
│       └── errors.py        # Error handlers
├── requirements.txt
└── README.md
```
