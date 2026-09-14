import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from state import AgentState

load_dotenv()


client = genai.Client(api_key=os.getenv("Auto-CEO"))


class MarketAnalysis(BaseModel):
    trend_summary: str = Field(description="Summary of current market trends")
    demand_direction: str = Field(description="High, Medium, or Low")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    recommendation: str = Field(description="Strategic market recommendation")

# 2. Define Market Agent Node Function
def market_agent_node(state: AgentState) -> dict:
    prompt = f"Analyze market signals for this business scenario: {state['scenario_input']}"
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MarketAnalysis,
            temperature=0.2,
        ),
    )
    
   
    return {"market_output": response.parsed.model_dump()}


if __name__ == "__main__":
    test_state: AgentState = {
        "scenario_input": "Demand for cloud AI software increased 25% this quarter, but hardware supply costs rose 10%.",
        "crisis_event": None,
        "market_output": None,
        "finance_output": None,
        "operations_output": None,
        "risk_output": None,
        "executive_decision": None
    }
    
    print("Running Market Agent Node...")
    result = market_agent_node(test_state)
    print("\n--- Market Agent Output (JSON) ---")
    print(result)