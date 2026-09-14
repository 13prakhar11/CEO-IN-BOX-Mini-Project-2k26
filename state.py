from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    scenario_input: str
    crisis_event: Optional[str]
    market_output: Optional[Dict[str, Any]]
    finance_output: Optional[Dict[str, Any]]
    operations_output: Optional[Dict[str, Any]]
    risk_output: Optional[Dict[str, Any]]
    executive_decision: Optional[Dict[str, Any]]
    