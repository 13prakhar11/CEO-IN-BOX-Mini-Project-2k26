from state import AgentState
from agents import finance_agent_node

if __name__ == "__main__":
    # 1. Define a complex financial crisis scenario
    test_input: AgentState = {
        "scenario_input": "Demand for electric vehicles increased by 40% this quarter, but lithium battery prices jumped 20%.",
        "crisis_event": "Unexpected 15% tariff imposed on raw material imports.",
        "market_output": None,
        "finance_output": None
    }

    print("Running Finance Agent (CFO)...\n")
    
    # 2. Execute the node
    result = finance_agent_node(test_input)

    # 3. Print the structured JSON results
    print("\n--- Final Finance Output Received ---")
    print(f"Health Status : {result['finance_output']['financial_health']}")
    print(f"Safe Budget   : {result['finance_output']['safe_budget_range']}")
    
    print("\nBudget Flags:")
    for flag in result['finance_output']['budget_flags']:
        print(f" - {flag}")
        
    print(f"\nRecommendation: {result['finance_output']['recommendation']}")