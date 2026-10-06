from langgraph.graph import StateGraph, START, END
from state import AgentState
from agents import (
    market_agent_node, 
    finance_agent_node, 
    operations_agent_node, 
    risk_agent_node, 
    executive_agent_node
)


builder = StateGraph(AgentState)

# 2. Add all worker nodes
builder.add_node("market", market_agent_node)
builder.add_node("finance", finance_agent_node)
builder.add_node("operations", operations_agent_node)
builder.add_node("risk", risk_agent_node)
builder.add_node("executive", executive_agent_node)

# 3. Parallel Fan-Out (Executes Market, Finance, Ops, and Risk simultaneously)
builder.add_edge(START, "market")
builder.add_edge(START, "finance")
builder.add_edge(START, "operations")
builder.add_edge(START, "risk")

# 4. Fan-In (Routes all outputs to the CEO node)
builder.add_edge("market", "executive")
builder.add_edge("finance", "executive")
builder.add_edge("operations", "executive")
builder.add_edge("risk", "executive")

# 5. Finalize execution path
builder.add_edge("executive", END)

# Compile into executable LangGraph app
app = builder.compile()

if __name__ == "__main__":
    print("--- Executing Auto-CEO Multi-Agent Pipeline ---\n")
    
    test_scenario: AgentState = {
        "scenario_input": "Demand for electric vehicles increased by 40% this quarter, but lithium battery prices jumped 20%.",
        "crisis_event": "Major port strike delaying international shipping by 3 weeks.",
        "market_output": None,
        "finance_output": None,
        "operations_output": None,
        "risk_output": None,
        "executive_decision": None
    }
    
    # Run graph execution
    final_output = app.invoke(test_scenario)
    
    print("\n==============================================")
    print("        FINAL EXECUTIVE BOARD RESOLUTION      ")
    print("==============================================\n")
    print("SYNTHESIS:")
    print(final_output["executive_decision"]["strategic_synthesis"])
    
    print("\nBOARD RESOLUTION:")
    print(final_output["executive_decision"]["final_board_resolution"])
    
    print("\nCRITICAL IMMEDIATE ACTIONS:")
    for action in final_output["executive_decision"]["critical_actions"]:
        print(f" - {action}")