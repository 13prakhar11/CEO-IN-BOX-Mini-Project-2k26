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
gemini_client = genai.Client(api_key=os.getenv("CEO_INBOX_GEMINI"))
groq_client = instructor.from_groq(Groq(api_key=os.getenv("CEO_INBOX_GROQ")))

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

class OperationsAnalysis(BaseModel):
    capacity_status: str = Field(description="Current operational capacity: Optimal, Strained, or Critical")
    supply_chain_impact: str = Field(description="Impact on supply chain and logistics")
    operational_risks: List[str] = Field(description="List of specific operational bottlenecks")
    recommendation: str = Field(description="Strategic operations recommendation")

class RiskComplianceAnalysis(BaseModel):
    overall_risk_level: str = Field(description="Low, Medium, High, or Severe")
    rule_violations: List[str] = Field(description="Potential regulatory or compliance violations")
    mitigation_strategy: str = Field(description="Steps to mitigate the identified risks")
    recommendation: str = Field(description="Strategic compliance recommendation")

class ExecutiveDecision(BaseModel):
    strategic_synthesis: str = Field(description="Brief synthesis of all departmental reports")
    final_board_resolution: str = Field(description="The ultimate strategic decision resolving any department conflicts")
    critical_actions: List[str] = Field(description="Top 3 immediate actions for the company to execute")

class EvaluationReport(BaseModel):
    faithfulness_score: float = Field(description="Score from 0.0 to 1.0 indicating if CEO's decision uses only factual department outputs without hallucinations.")
    conflict_resolution_score: float = Field(description="Score from 0.0 to 1.0 indicating if department conflicts were successfully resolved.")
    verdict: str = Field(description="Must be 'PASSED' or 'NEEDS_REVISION'")
    evaluation_summary: str = Field(description="Detailed explanation justifying the scores")


# --- 3. UNIVERSAL FAILOVER ROUTER ---
def call_llm_with_fallback(prompt: str, schema: Type[BaseModel], system_role: str) -> BaseModel:
    """Universal router that attempts Gemini first, falls back to Groq for ANY agent."""
    try:
        print(f"[LLM Router] Attempting Gemini for {schema.__name__}...")
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
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
        print("[LLM Router] Switching to Fallback Provider: Groq (openai/gpt-oss-120b)...\n")
        
        groq_response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
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
        f"Specific Board Question: {state.get('user_query', 'N/A')}\n"
    )
    system_role = "You are an expert Chief Financial Officer (CFO). Assess financial risks and output valid JSON."
    
    finance_data = call_llm_with_fallback(prompt, FinanceAnalysis, system_role)
    return {"finance_output": finance_data.model_dump()}

def operations_agent_node(state: AgentState) -> dict:
    prompt = (
        f"Analyze the operational and supply chain impact for this scenario: {state['scenario_input']}. "
        f"Crisis event context: {state.get('crisis_event', 'None')}"
        f"Specific Board Question: {state.get('user_query', 'N/A')}\n"
    )
    system_role = "You are an expert Chief Operating Officer (COO). Assess capacity and supply chain logistics. Output valid JSON."
    
    ops_data = call_llm_with_fallback(prompt, OperationsAnalysis, system_role)
    return {"operations_output": ops_data.model_dump()}

def risk_agent_node(state: AgentState) -> dict:
    prompt = (
        f"Analyze the regulatory, legal, and overall business risks for this scenario: {state['scenario_input']}. "
        f"Crisis event context: {state.get('crisis_event', 'None')}"
        f"Specific Board Question: {state.get('user_query', 'N/A')}\n"
    )
    system_role = "You are an expert Chief Compliance Officer (CCO). Assess legal and regulatory risks. Output valid JSON."
    
    risk_data = call_llm_with_fallback(prompt, RiskComplianceAnalysis, system_role)
    return {"risk_output": risk_data.model_dump()}

def executive_agent_node(state: AgentState) -> dict:
    prompt = (
        f"Scenario: {state['scenario_input']}\n"
        f"Crisis Event: {state.get('crisis_event', 'None')}\n\n"
        f"Market Dept: {state.get('market_output')}\n"
        f"Finance Dept: {state.get('finance_output')}\n"
        f"Operations Dept: {state.get('operations_output')}\n"
        f"Risk Dept: {state.get('risk_output')}\n\n"
        f"Specific Board Question: {state.get('user_query', 'N/A')}\n\n"
        "As the CEO, synthesize these reports, resolve any conflicting advice, and output a final strategic resolution."
    )
    system_role = "You are the CEO of a Fortune 500 company. Output valid JSON."
    
    exec_data = call_llm_with_fallback(prompt, ExecutiveDecision, system_role)
    return {"executive_decision": exec_data.model_dump()}

def evaluator_agent_node(state: AgentState) -> dict:
    prompt = (
        f"Original Scenario: {state['scenario_input']}\n"
        f"Crisis Event: {state.get('crisis_event', 'None')}\n\n"
        f"Specialist Department Outputs:\n"
        f"- Market: {state.get('market_output')}\n"
        f"- Finance: {state.get('finance_output')}\n"
        f"- Operations: {state.get('operations_output')}\n"
        f"- Risk: {state.get('risk_output')}\n\n"
        f"CEO Executive Decision to Audit:\n"
        f"{state.get('executive_decision')}\n\n"
        "Audit the CEO's executive decision against the department data. Verify:\n"
        "1. Faithfulness: Are all financial numbers, timelines, and risks grounded directly in department reports?\n"
        "2. Conflict Resolution: Did the CEO address conflicting goals between departments?\n"
        "Output your score and verdict."
    )
    system_role = "You are an independent Corporate Governance Auditor. Grade decisions strictly and output valid JSON."
    
    eval_data = call_llm_with_fallback(prompt, EvaluationReport, system_role)
    return {"evaluation_report": eval_data.model_dump()}

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# ==========================================
# GRAPH ORCHESTRATION & ROUTING
# ==========================================

# 1. Initialize the SQLite permanent memory checkpointer
conn = sqlite3.connect("auto_ceo_memory.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

# 2. Initialize the graph using your AgentState schema
builder = StateGraph(AgentState)

# 3. Add all your specialist and executive nodes to the graph
# (Ensure these string names match your actual function names above)
builder.add_node("market", market_agent_node)
builder.add_node("finance", finance_agent_node)
builder.add_node("operations", operations_agent_node)
builder.add_node("risk", risk_agent_node)
builder.add_node("executive", executive_agent_node)
builder.add_node("evaluator", evaluator_agent_node)

# 4. Define the Parallel Flow (Edges)
# FAN-OUT: The START node sends the crisis to all 4 departments at the same time
builder.add_edge(START, "market")
builder.add_edge(START, "finance")
builder.add_edge(START, "operations")
builder.add_edge(START, "risk")

# FAN-IN: All 4 departments must finish before passing data to the CEO
builder.add_edge("market", "executive")
builder.add_edge("finance", "executive")
builder.add_edge("operations", "executive")
builder.add_edge("risk", "executive")

# CEO passes the final resolution to the Auditor for scoring
builder.add_edge("executive", "evaluator")

# Auditor finishes the pipeline
builder.add_edge("evaluator", END)

# 5. Compile the entire network into the variable app.py is looking for
auto_ceo_graph = builder.compile(checkpointer=memory)