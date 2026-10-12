import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from main import app as langgraph_app

app = Flask(__name__)
# SECURITY: Cryptographic key for session cookies (In production, use a .env variable)
app.secret_key = "enterprise_super_secret_key_2026"

# Hardcoded credentials for the mini-project (Admin level)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# --- Security Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            session["role"] = "Administrator"
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "error")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    result = None
    if request.method == "POST":
        scenario = request.form.get("scenario", "")
        crisis = request.form.get("crisis", "")
        user_query = request.form.get("user_query", "")
        session_id = request.form.get("session_id", "default_session")

        initial_state = {
            "scenario_input": scenario,
            "crisis_event": crisis,
            "user_query": user_query
        }
        config = {"configurable": {"thread_id": session_id}}

        final_state = langgraph_app.invoke(initial_state, config=config)

        result = {
            "decision": final_state.get("executive_decision", {}),
            "audit": final_state.get("evaluation_report", {})
        }
    return render_template("dashboard.html", result=result)

@app.route("/admin")
@login_required
def admin():
    # Fetch historical data directly from the LangGraph SQLite database
    sessions = []
    try:
        conn = sqlite3.connect("auto_ceo_memory.sqlite")
        cursor = conn.cursor()
        # Query unique session IDs
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints;")
        rows = cursor.fetchall()
        sessions = [row[0] for row in rows]
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")
        
    return render_template("admin.html", sessions=sessions)

if __name__ == "__main__":
    app.run(debug=True, port=5000)