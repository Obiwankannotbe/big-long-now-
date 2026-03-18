###this is hte main file for the CTF question, fully working//....

from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "nirvana1994grunge"
DB_PATH = "nirvana.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── Home / Search ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    q = request.args.get("q", "")
    results = []
    spelling = "colour"   # default British spelling = "true" oracle

    if q:
        conn = get_db()
        cursor = conn.cursor()
        # VULNERABLE: raw f-string, no sanitisation
        raw_query = f"SELECT * FROM songs WHERE title LIKE '%{q}%' "
        try:
            cursor.execute(raw_query)
            rows = cursor.fetchall()
            if rows:
                spelling = "colour"   # result found  → British
            else:
                spelling = "color"    # no result     → American
            results = rows
        except Exception:
            spelling = "color"        # error also counts as false
        conn.close()

    return render_template("index.html", q=q, results=results, spelling=spelling)

# ── Admin Login ────────────────────────────────────────────────────────────────
@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admin WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            session["admin"] = True
            return redirect(url_for("flag"))
        else:
            error = "Invalid credentials."
    return render_template("admin.html", error=error)

# ── Flag Page ──────────────────────────────────────────────────────────────────
@app.route("/flag")
def flag():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    return render_template("flag.html")

# ── Logout ─────────────────────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("[!] Database not found. Run: python setup_db.py")
        exit(1)
    app.run(debug=False, host="0.0.0.0", port=5000)