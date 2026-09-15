import os
import instructor
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq
from pydantic import BaseModel, Field
from typing import TypedDict, Optional, Dict, Any

# 1. Load Environment Variables & Initialize Clients
load_dotenv()

# Primary Client: Gemini
gemini_client = genai.Client(api_key=os.getenv("CEO-inbox"))

# Fallback Client: Groq (wrapped with Instructor for Pydantic enforcement)
groq_client = instructor.from_groq(Groq(api_key=os.getenv("CEO-inbox")))


# 2. Shared State Definition
class AgentState(TypedDict):
    scenario_input: str
    crisis_event: Optional[str]
    market_output: Optional[Dict[str, Any]]


# 3. Pydantic Form Schema
class MarketAnalysis(BaseModel):
    trend_summary: str = Field(description="Summary of current market trends")
    demand_direction: str = Field(description="High, Medium, or Low")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    recommendation: str = Field(description="Strategic market recommendation")


# 4. Fallback LLM Calling Function
def call_market_llm_with_fallback(prompt: str) -> MarketAnalysis:
    """
    Attempts to call Gemini first. 
    If Gemini throws a 503 or any API exception, falls back to Groq.
    """
    try:
        print("[LLM Router] Attempting primary call with Gemini (gemini-3.6-flash)...")
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MarketAnalysis,
                temperature=0.2,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            ),
        )
        print("[LLM Router] Success using Gemini!")
        return response.parsed

    except Exception as e:
        print(f"\n[LLM Router WARNING] Gemini call failed with error: {e}")
        print("[LLM Router] Switching to Fallback Provider: Groq (llama-3.3-70b-versatile)...\n")
        
        # Fallback call to Groq
        groq_response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            response_model=MarketAnalysis,
            messages=[
                {"role": "system", "content": "You are an expert corporate market analyst. Output valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        print("[LLM Router] Success using Groq Fallback!")
        return groq_response


# 5. Agent Node Function
def market_agent_node(state: AgentState) -> dict:
    prompt = f"Analyze market signals for this business scenario: {state['scenario_input']}"
    
    # Call the router function with built-in fallback
    market_data: MarketAnalysis = call_market_llm_with_fallback(prompt)
    
    return {"market_output": market_data.model_dump()}


# ---------------------------------------------------------
# DIRECT TEST RUNNER
# ---------------------------------------------------------
if __name__ == "__main__":
    test_input: AgentState = {
        "scenario_input": "Indian stock market is experiencing a 15% surge in tech stocks, but global inflation concerns are rising.",
        "crisis_event": None,
        "market_output": None
    }

    print("Running Market Agent with Auto-Failover...\n")
    result = market_agent_node(test_input)

    print("\n--- Final Agent Output Received ---")
    print(f"Trend Summary : {result['market_output']['trend_summary']}")
    print(f"Demand        : {result['market_output']['demand_direction']}")
    print(f"Confidence    : {result['market_output']['confidence']}")
    print(f"Recommendation: {result['market_output']['recommendation']}")