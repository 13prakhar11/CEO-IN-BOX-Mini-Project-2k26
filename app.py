import sqlite3
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

# IMPORT YOUR LANGGRAPH WORKFLOW HERE
# Change 'agents' and 'auto_ceo_graph' to match your actual file and graph variable names
from agents import auto_ceo_graph 

app = Flask(__name__)
# Secret key is required for Flask session (login) management
app.secret_key = "super_secret_enterprise_key" 

# ==========================================
# 1. AUTHENTICATION GATEWAY
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check database for user credentials
        conn = sqlite3.connect("auto_ceo_memory.sqlite")
        cursor = conn.cursor()
        
        # We check if the users table exists first, just in case init_db.py wasn't run
        try:
            cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
        except sqlite3.OperationalError:
            flash('Database not initialized. Please run init_db.py first.')
            return render_template('login.html')
        finally:
            conn.close()
        
        if user:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = user[0] # 'admin' or 'user'
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Access denied.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==========================================
# 2. MAIN EXECUTIVE SIMULATOR (DASHBOARD)
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # Protect route: Kick unauthenticated users back to login
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    result = None
    
    if request.method == 'POST':
        # Grab inputs from the dark-mode UI
        scenario = request.form.get('scenario')
        crisis = request.form.get('crisis')
        user_query = request.form.get('user_query')
        raw_session_id = request.form.get('session_id')
        
        # Inject inputs into the LangGraph state
        initial_state = {
            "scenario_input": scenario,
            "crisis_event": crisis,
            "user_query": user_query
        }
        
        # MARKET-READY FIX: Tag the thread_id with the username to track ownership
        # E.g., if client1 enters 'SESS_005', it saves as 'client1_SESS_005'
        secure_thread_id = f"{session['username']}_{raw_session_id}"
        config = {"configurable": {"thread_id": secure_thread_id}}
        
        # Execute the multi-agent pipeline
        final_state = auto_ceo_graph.invoke(initial_state, config=config)
        
        # Extract all department briefings and final CEO/Auditor decisions
        result = {
            "market": final_state.get("market_output", {}),
            "finance": final_state.get("finance_output", {}),
            "operations": final_state.get("operations_output", {}),
            "risk": final_state.get("risk_output", {}),
            "decision": final_state.get("executive_decision", {}),
            "audit": final_state.get("evaluation_report", {})
        }
        
    return render_template("dashboard.html", result=result)

# ==========================================
# 3. SYSTEM LOGS & USER HISTORY
# ==========================================
@app.route('/history')
def user_history():
    # Private history for standard users
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    logs = fetch_logs(filter_user=session['username'])
    return render_template('admin.html', logs=logs, page_title="My Run History")

@app.route('/admin')
def admin_panel():
    # Global tracking for Admins only
    if not session.get('logged_in') or session.get('role') != 'admin':
        return "Unauthorized Access. Administrator privileges required.", 403

    logs = fetch_logs(filter_user=None) # Fetch everything
    return render_template('admin.html', logs=logs, page_title="Global System Logs")

def fetch_logs(filter_user=None):
    """Helper function to pull and decode LangGraph states via get_state()"""
    logs = []
    try:
        conn = sqlite3.connect("auto_ceo_memory.sqlite")
        cursor = conn.cursor()
        
        # If standard user, only fetch threads starting with their username
        if filter_user:
            cursor.execute("SELECT DISTINCT thread_id FROM checkpoints WHERE thread_id LIKE ? ORDER BY thread_id DESC", (f"{filter_user}_%",))
        else:
            # If admin, fetch all threads
            cursor.execute("SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id DESC")
            
        rows = cursor.fetchall()
        
        for row in rows:
            thread_id = row[0]
            
            # Let LangGraph handle the secure decoding of the binary data
            config = {"configurable": {"thread_id": thread_id}}
            state_snapshot = auto_ceo_graph.get_state(config)
            state_values = state_snapshot.values
            
            if state_values:
                # Strip the username prefix for display purposes on the frontend
                display_thread = thread_id.split('_', 1)[-1] if '_' in thread_id else thread_id
                
                logs.append({
                    "owner": thread_id.split('_')[0] if '_' in thread_id else "unknown",
                    "thread_id": display_thread,
                    "scenario": state_values.get("scenario_input", "No scenario found"),
                    "resolution": state_values.get("executive_decision", {}).get("final_board_resolution", "Pending..."),
                    "verdict": state_values.get("evaluation_report", {}).get("verdict", "N/A")
                })
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            
    return logs

if __name__ == '__main__':
    app.run(debug=True, port=5000)