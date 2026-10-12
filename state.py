from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    scenario_input: str
    crisis_event: Optional[str]
    user_query: Optional[str]  # <--- ADD THIS LINE
    market_output: Optional[Dict[str, Any]]
    finance_output: Optional[Dict[str, Any]]
    operations_output: Optional[Dict[str, Any]]
    risk_output: Optional[Dict[str, Any]]
    executive_decision: Optional[Dict[str, Any]]
    evaluation_report: Optional[Dict[str, Any]]
    