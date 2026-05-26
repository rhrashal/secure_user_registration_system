import os, re, sqlite3, hashlib
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


def validate(field_id, value):
    msg = ""
    if field_id == "fullName":
        if not value:
            msg = "Full Name is required."
        elif not re.match(r"^[a-zA-Z\s\.]+$", value):
            msg = "Only letters, spaces, and dots allowed."
        elif len(value) < 2:
            msg = "Must be at least 2 characters."
    elif field_id in ("email", "loginEmail"):
        if not value:
            msg = "Email is required."
        elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", value):
            msg = "Enter a valid email address."
    elif field_id == "phone":
        if not value:
            msg = "Phone number is required."
        elif not re.match(r"^[\d\s\+\-\(\)]{7,15}$", value):
            msg = "Enter a valid phone number (7-15 digits)."
    elif field_id in ("password", "loginPassword"):
        if not value:
            msg = "Password is required."
        elif len(value) < 8:
            msg = "Must be at least 8 characters."
        elif not re.search(r"[A-Z]", value):
            msg = "Must contain an uppercase letter."
        elif not re.search(r"[a-z]", value):
            msg = "Must contain a lowercase letter."
        elif not re.search(r"[0-9]", value):
            msg = "Must contain a number."
        elif not re.search(r"[!@#$%^&*]", value):
            msg = "Must contain a special character (!@#$%^&*)."
    return msg


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    errors = {}
    if request.method == "POST":
        fields = {
            "fullName": request.form.get("fullName", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "password": request.form.get("password", ""),
        }
        for fid, val in fields.items():
            e = validate(fid, val)
            if e:
                errors[fid] = e

        if not errors:
            conn = get_db()
            existing = conn.execute(
                "SELECT email FROM users WHERE email = ?", (fields["email"],)
            ).fetchone()
            if existing:
                errors["email"] = "Email already registered."
            else:
                pw_hash = hash_password(fields["password"])
                conn.execute(
                    "INSERT INTO users (email, full_name, phone, password_hash) VALUES (?, ?, ?, ?)",
                    (fields["email"], fields["fullName"], fields["phone"], pw_hash),
                )
                conn.commit()
                conn.close()
                return redirect(url_for("login"))
            conn.close()

    return render_template("register.html", errors=errors)


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = {}
    if request.method == "POST":
        email = request.form.get("loginEmail", "").strip()
        password = request.form.get("loginPassword", "")

        e1 = validate("loginEmail", email)
        e2 = validate("loginPassword", password)
        if e1:
            errors["loginEmail"] = e1
        if e2:
            errors["loginPassword"] = e2

        if not errors:
            conn = get_db()
            row = conn.execute(
                "SELECT password_hash FROM users WHERE email = ?", (email,)
            ).fetchone()
            conn.close()
            if row and row["password_hash"] == hash_password(password):
                session["email"] = email
                return redirect(url_for("dashboard"))
            else:
                errors["login"] = "Invalid Email or Password"

    return render_template("login.html", errors=errors)


@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    users = conn.execute(
        "SELECT email, full_name, phone, password_hash FROM users ORDER BY email"
    ).fetchall()
    conn.close()
    return render_template("dashboard.html", users=users, email=session["email"])


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
