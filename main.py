import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from state import AgentState
from agents import (
    market_agent_node, 
    finance_agent_node, 
    operations_agent_node, 
    risk_agent_node, 
    executive_agent_node,
    evaluator_agent_node  # NEW
)

# 1. Initialize StateGraph
builder = StateGraph(AgentState)

# 2. Add all nodes
builder.add_node("market", market_agent_node)
builder.add_node("finance", finance_agent_node)
builder.add_node("operations", operations_agent_node)
builder.add_node("risk", risk_agent_node)
builder.add_node("executive", executive_agent_node)
builder.add_node("evaluator", evaluator_agent_node)  # NEW

# 3. Parallel Fan-Out
builder.add_edge(START, "market")
builder.add_edge(START, "finance")
builder.add_edge(START, "operations")
builder.add_edge(START, "risk")

# 4. Fan-In to Executive
builder.add_edge("market", "executive")
builder.add_edge("finance", "executive")
builder.add_edge("operations", "executive")
builder.add_edge("risk", "executive")

# 5. Executive to Evaluator to END
builder.add_edge("executive", "evaluator")  # NEW
builder.add_edge("evaluator", END)          # NEW

# ==========================================
# DATABASE MEMORY LAYER
# ==========================================
db_conn = sqlite3.connect("auto_ceo_memory.sqlite", check_same_thread=False)
memory = SqliteSaver(db_conn)
memory.setup()

app = builder.compile(checkpointer=memory)

if __name__ == "__main__":
    print("--- Executing Auto-CEO with Auditor Agent ---\n")
    
    test_scenario = {
        "scenario_input": "Demand for electric vehicles increased by 40% this quarter, but lithium battery prices jumped 20%.",
        "crisis_event": "Major port strike delaying international shipping by 3 weeks.",
        "market_output": None,
        "finance_output": None,
        "operations_output": None,
        "risk_output": None,
        "executive_decision": None,
        "evaluation_report": None
    }
    
    config = {"configurable": {"thread_id": "eval_test_001"}}
    final_output = app.invoke(test_scenario, config=config)
    
    decision = final_output["executive_decision"]
    audit = final_output["evaluation_report"]
    
    print("\n==============================================")
    print("        FINAL EXECUTIVE BOARD RESOLUTION      ")
    print("==============================================\n")
    print("SYNTHESIS:")
    print(decision["strategic_synthesis"])
    
    print("\n==============================================")
    print("             AUDITOR AGENT REPORT             ")
    print("==============================================\n")
    print(f"VERDICT: {audit['verdict']}")
    print(f"Faithfulness Score: {audit['faithfulness_score']} / 1.0")
    print(f"Conflict Resolution Score: {audit['conflict_resolution_score']} / 1.0")
    print(f"Summary: {audit['evaluation_summary']}")