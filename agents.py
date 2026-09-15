import os
import instructor
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq
from pydantic import BaseModel, Field
from typing import List, Type, Any
from state import AgentState

# --- 1. LOAD CLIENTS ---
load_dotenv()
gemini_client = genai.Client(api_key=os.getenv("CEO-inbox"))
groq_client = instructor.from_groq(Groq(api_key=os.getenv("CEO-inbox")))

# --- 2. PYDANTIC SCHEMAS ---
class MarketAnalysis(BaseModel):
    trend_summary: str = Field(description="Summary of current market trends")
    demand_direction: str = Field(description="High, Medium, or Low")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    recommendation: str = Field(description="Strategic market recommendation")

class FinanceAnalysis(BaseModel):
    financial_health: str = Field(description="Overall health: Stable, At Risk, or Critical")
    safe_budget_range: str = Field(description="Estimated safe budget allocation range in USD")
    budget_flags: List[str] = Field(description="List of specific financial risks or warnings")
    recommendation: str = Field(description="Strategic financial recommendation")

# --- 3. UNIVERSAL FAILOVER ROUTER ---
def call_llm_with_fallback(prompt: str, schema: Type[BaseModel], system_role: str) -> BaseModel:
    """Universal router that attempts Gemini first, falls back to Groq for ANY agent."""
    try:
        print(f"[LLM Router] Attempting Gemini for {schema.__name__}...")
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.2,
                system_instruction=system_role,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            ),
        )
        print("[LLM Router] Success using Gemini!")
        return response.parsed

    except Exception as e:
        print(f"\n[LLM Router WARNING] Gemini call failed: {e}")
        print("[LLM Router] Switching to Fallback Provider: Groq (openai/gpt-oss-20b)...\n")
        
        groq_response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            response_model=schema,
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ]
        )
        print("[LLM Router] Success using Groq Fallback!")
        return groq_response

# --- 4. AGENT NODES ---
def market_agent_node(state: AgentState) -> dict:
    prompt = f"Analyze market signals for this business scenario: {state['scenario_input']}"
    system_role = "You are an expert corporate market analyst. Output valid JSON."
    
    market_data = call_llm_with_fallback(prompt, MarketAnalysis, system_role)
    return {"market_output": market_data.model_dump()}

def finance_agent_node(state: AgentState) -> dict:
    prompt = (
        f"Analyze the financial impact and budget constraints for this business scenario: {state['scenario_input']}. "
        f"Consider any crisis events if applicable: {state.get('crisis_event', 'None')}"
    )
    system_role = "You are an expert Chief Financial Officer (CFO). Assess financial risks and output valid JSON."
    
    finance_data = call_llm_with_fallback(prompt, FinanceAnalysis, system_role)
    return {"finance_output": finance_data.model_dump()}