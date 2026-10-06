from state import AgentState
from agents import operations_agent_node

if __name__ == "__main__":
    # Define the test scenario
    test_input: AgentState = {
        "scenario_input": "Demand for electric vehicles increased by 40% this quarter, but lithium battery prices jumped 20%.",
        "crisis_event": "Major port strike delaying international shipping by 3 weeks.",
        "market_output": None,
        "finance_output": None,
        "operations_output": None,
        "risk_output": None,
        "executive_decision": None
    }

    print("Running Operations Agent (COO)...\n")
    
    # Execute the node
    result = operations_agent_node(test_input)

    # Print the structured JSON results
    print("\n--- Final Operations Output Received ---")
    print(f"Capacity Status    : {result['operations_output']['capacity_status']}")
    print(f"Supply Chain Impact: {result['operations_output']['supply_chain_impact']}")
    
    print("\nOperational Risks:")
    for risk in result['operations_output']['operational_risks']:
        print(f" - {risk}")
        
    print(f"\nRecommendation: {result['operations_output']['recommendation']}")