import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "labdb")
DB_USER = os.getenv("DB_USER", "labuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "labpass")

DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "compose-lab-secret")

engine = create_engine(DATABASE_URI, pool_pre_ping=True, pool_size=5, max_overflow=10)

# Create table if not exists
CREATE_TABLE_SQL = text('''
CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
''')

with engine.begin() as conn:
    conn.execute(CREATE_TABLE_SQL)

def db_connected():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    status = db_connected()
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not full_name or not email:
            flash("Full name and email are required.", "danger")
            return redirect(url_for("index"))

        try:
            with engine.begin() as conn:
                conn.execute(
                    text("INSERT INTO submissions (full_name, email, message) VALUES (:n, :e, :m)"),
                    {"n": full_name, "e": email, "m": message},
                )
            flash("Submission saved.", "success")
            return redirect(url_for("index"))
        except SQLAlchemyError as e:
            flash(f"Database error: {e}", "danger")
            return redirect(url_for("index"))

    rows = []
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, full_name, email, message, created_at FROM submissions ORDER BY id DESC"))
            rows = list(result.fetchall())
    except SQLAlchemyError as e:
        flash(f"Could not load rows: {e}", "warning")

    return render_template("index.html", rows=rows, connected=status)

@app.route("/health")
def health():
    return {"web": "ok", "db_connected": db_connected()}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
