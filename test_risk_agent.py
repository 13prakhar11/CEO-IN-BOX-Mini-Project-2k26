from state import AgentState
from agents import risk_agent_node

if __name__ == "__main__":
    # Define the test scenario
    test_input: AgentState = {
        "scenario_input": "Demand for electric vehicles increased by 40% this quarter, but lithium battery prices jumped 20%.",
        "crisis_event": "New EU environmental regulations ban the current battery chemical compound.",
        "market_output": None,
        "finance_output": None,
        "operations_output": None,
        "risk_output": None,
        "executive_decision": None
    }

    print("Running Risk & Compliance Agent (CCO)...\n")
    
    # Execute the node
    result = risk_agent_node(test_input)

    # Print the structured JSON results
    print("\n--- Final Risk Output Received ---")
    print(f"Overall Risk Level  : {result['risk_output']['overall_risk_level']}")
    
    print("\nRule Violations:")
    for rule in result['risk_output']['rule_violations']:
        print(f" - {rule}")
        
    print(f"\nMitigation Strategy : {result['risk_output']['mitigation_strategy']}")
    print(f"Recommendation      : {result['risk_output']['recommendation']}")