import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import TypedDict, Optional, Dict, Any


load_dotenv()
client = genai.Client(api_key=os.getenv("Auto-CEO"))


class AgentState(TypedDict):
    scenario_input: str
    crisis_event: Optional[str]
    market_output: Optional[Dict[str, Any]]


class MarketAnalysis(BaseModel):
    trend_summary: str = Field(description="Summary of current market trends")
    demand_direction: str = Field(description="High, Medium, or Low")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    recommendation: str = Field(description="Strategic market recommendation")


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
    # Create fake business input data
    test_input: AgentState = {
        "scenario_input": "Demand for electric vehicles increased by 40% this quarter, but lithium battery prices jumped 20%.",
        "crisis_event": None,
        "market_output": None
    }

    print("Sending test scenario to Market Agent...\n")
    

    result = market_agent_node(test_input)

  
    print("--- SUCCESS! Agent Output Received ---")
    print(f"Trend Summary : {result['market_output']['trend_summary']}")
    print(f"Demand        : {result['market_output']['demand_direction']}")
    print(f"Confidence    : {result['market_output']['confidence']}")
    print(f"Recommendation: {result['market_output']['recommendation']}")