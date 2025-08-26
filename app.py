from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import socket

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT,
                 points INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 training_type TEXT,
                 minutes INTEGER,
                 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("soccer.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists!"
        conn.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("soccer.db")
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials!"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE id=?", (session["user_id"],))
    points = c.fetchone()[0]
    c.execute("SELECT training_type, minutes, date FROM logs WHERE user_id=? ORDER BY date DESC", (session["user_id"],))
    logs = c.fetchall()
    conn.close()
    return render_template("dashboard.html", points=points, logs=logs)

@app.route("/log", methods=["POST"])
def log_training():
    if "user_id" not in session:
        return redirect(url_for("login"))
    training_type = request.form["training_type"]
    minutes = int(request.form["minutes"])
    points_earned = minutes
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, training_type, minutes) VALUES (?, ?, ?)", (session["user_id"], training_type, minutes))
    c.execute("UPDATE users SET points = points + ? WHERE id=?", (points_earned, session["user_id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

# --- Auto Free Port ---
def find_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
