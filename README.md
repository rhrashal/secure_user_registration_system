# Secure User Registration System — Python (Flask) Edition

A server-side Python port of the original client-side user registration system. Built with Flask, SQLite, and SHA-512 password hashing.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.14+ | Runtime |
| Flask 3.x | Web framework (routing, sessions, templates) |
| SQLite3 | Database (file-based, no server needed) |
| hashlib (SHA-512) | Password hashing |
| Jinja2 | Server-side HTML templating |
| HTML5 / CSS3 / Vanilla JS | Frontend (dark mode, password strength, inline validation) |

## Project Structure

```
python/
├── app.py                 Flask application — all routes, validation, DB logic
├── requirements.txt       Python dependencies
├── users.db               SQLite database file (auto-created on first run)
├── README.md              This file
├── templates/
│   ├── base.html          Base layout (dark mode toggle, footer, JS)
│   ├── index.html         Home page with Register / Login buttons
│   ├── register.html      Registration form
│   ├── login.html         Login form
│   └── dashboard.html     Post-login dashboard showing all users
└── static/
    ├── style.css          Complete styling (light + dark mode)
    └── script.js          Client-side: dark mode, password strength, field validation
```

## Features

- **User Registration** — Full Name, Email, Phone, Password
- **Server-side Validation** — All fields validated before insert (also duplicated client-side for UX)
- **Password Strength Indicator** — Real-time Weak / Medium / Strong meter
- **SHA-512 Hashing** — Passwords hashed server-side with `hashlib.sha512` before storage
- **SQLite Persistence** — Data stored in `users.db` on disk (survives server restarts)
- **Flask Session Auth** — Login state tracked via signed session cookies
- **Dashboard** — After login, view all registered users with their email, name, phone, and password hash
- **Dark Mode** — Toggle persisted in `localStorage`
- **Duplicate Email Check** — Registration rejects already-registered emails

## How to Run

### 1. Install dependencies

```bash
cd python
python -m pip install -r requirements.txt
```

### 2. Start the server

```bash
python app.py
```

The app starts at **http://localhost:5000**.

> `users.db` is created automatically in the `python/` directory on first request.

### 3. Usage

1. Open http://localhost:5000 in a browser
2. Click **Register** and fill out the form
3. After successful registration, you are redirected to **Login**
4. Log in with your email and password
5. View the **Dashboard** showing all registered users
6. Click **Logout** to end the session

## Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Home page |
| GET | `/register` | Show registration form |
| POST | `/register` | Validate fields, hash password, insert into DB, redirect to login |
| GET | `/login` | Show login form |
| POST | `/login` | Validate credentials, set session, redirect to dashboard |
| GET | `/dashboard` | Show all users (requires session) |
| GET | `/logout` | Clear session, redirect to home |
| Any | `/*` (404) | Catch-all — redirects to `/` (index) |

## Database Schema

```sql
CREATE TABLE users (
    email         TEXT PRIMARY KEY,
    full_name     TEXT NOT NULL,
    phone         TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

```

## Field Validation Rules

| Field | Rules |
|-------|-------|
| Full Name | Required, letters/spaces/dots only, min 2 characters |
| Email | Required, valid email format, must be unique |
| Phone | Required, digits/spaces/+-/parentheses, 7-15 characters |
| Password | Required, min 8 characters, must include uppercase, lowercase, digit, and special character (!@#$%^&*) |

## Security Notes

- **Passwords are never stored in plain text.** They are SHA-512 hashed before storage.
- **SQL injection is prevented.** All queries use parameterized statements (`?` placeholders).
- **Session security.** Flask signs the session cookie with a random `secret_key` generated at startup.
- **This is a learning/demo project.** For production, use bcrypt/argon2, HTTPS, rate limiting, and CSRF protection.

## Comparison with Original JS Version

| Aspect | Original (JS / client-side) | Python (Flask / server-side) |
|--------|-----------------------------|------------------------------|
| Database | sql.js (WASM in browser) + IndexedDB | Python `sqlite3` → `users.db` file |
| Hashing | Web Crypto API (`crypto.subtle.digest`) | `hashlib.sha512()` |
| Auth/State | Query string in URL | Flask signed session cookie |
| Templates | Plain HTML | Jinja2 templates (Flask) |
| Validation | JavaScript only | Python server-side + JS client-side |
| Persistence | IndexedDB (browser storage) | On-disk `.db` file |

## Assignment Details

| Field | Value |
|-------|-------|
| Course | Network Security |
| Code | 115 |
| Submission | 11 June 2026 |
| Submitted To | Dr. Risala Tasin Khan, Professor, Jahangirnagar University |
| Submitted By | ROBIUL HOSSAIN, ID: 25306, PGDIT, IIT, Jahangirnagar University |
