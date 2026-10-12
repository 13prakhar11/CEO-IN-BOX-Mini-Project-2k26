from main import app  # Imports your LangGraph engine

# Enter the Session ID you used on the web dashboard
session_id = "boardroom_session_003" 

# Configure LangGraph to look up that specific session
config = {"configurable": {"thread_id": session_id}}

# Fetch the historical memory from the SQLite database
saved_data = app.get_state(config)

print(f"--- MEMORY LOG FOR SESSION: {session_id} ---")
print(f"Saved Scenario: {saved_data.values.get('scenario_input')}")
print(f"Saved Crisis: {saved_data.values.get('crisis_event')}")
print(f"Saved User Query: {saved_data.values.get('user_query')}")