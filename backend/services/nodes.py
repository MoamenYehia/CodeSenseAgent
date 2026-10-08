import os
from typing import Literal
from dotenv import load_dotenv

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langgraph.types import interrupt

from services.state import SalesState
from services.tools.calender_booking_tool import calendar_booking_tool
from services.tools.company_enrichment_tool import company_enrichment_tool
from services.tools.crm_lead_recorder import crm_lead_recorder
from services.tools.rag_tool import rag_tool

load_dotenv()

# 1. Tools definition & standard ToolNode
sales_tools = [calendar_booking_tool, company_enrichment_tool, crm_lead_recorder, rag_tool]
tools_node = ToolNode(sales_tools)


# 2. Sales Agent Node
def sales_agent_node(state: SalesState, config: RunnableConfig = None):
    llm = ChatGroq(
        model="qwen/qwen3.8-27b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )
    llm_with_tools = llm.bind_tools(sales_tools)

    system_prompt = SystemMessage(content=(
        "You are CodeSense AI's top B2B Senior Sales Engineer.\n"
        "Your objective is to qualify leads, match them to the correct pricing tier (Solo, Team, Enterprise), "
        "and guide them toward booking a demo or recording their lead in the CRM.\n\n"
        "Execution Rules:\n"
        "1. Always consult `rag_tool` for authoritative pricing, features, and policy rules.\n"
        "2. When a user provides a work email or company domain, invoke `company_enrichment_tool` to check headcount.\n"
        "3. Match the user to Team Tier (2-25 devs) or Enterprise Tier (>25 devs or compliance/on-prem needs).\n"
        "4. Be professional, concise, and helpful."
    ))

    messages = [system_prompt] + list(state["messages"])
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# 3. Lead Evaluator Node
def lead_evaluator_node(state: SalesState):
    messages = state.get("messages", [])
    if not messages:
        return {}

    requires_human_escalation = False
    escalation_reason = None

    # Filter ONLY human messages (ignore system and AI messages)
    human_text = " ".join([
        m.content.lower() for m in messages 
        if isinstance(m, HumanMessage) and isinstance(m.content, str)
    ])

    # Check if the HUMAN asked for enterprise custom contracts or on-premise setups
    if "enterprise" in human_text and any(k in human_text for k in ["custom contract", "escalat", "sales director"]):
        requires_human_escalation = True
        escalation_reason = "High-value Enterprise deal identified requiring Sales Director custom approval."
    elif any(k in human_text for k in ["on-premise", "on premise", "air-gapped", "soc2 report"]):
        requires_human_escalation = True
        escalation_reason = "Custom compliance or On-Premise deployment requested."

    return {
        "requires_human_escalation": requires_human_escalation,
        "escalation_reason": escalation_reason
    }


# 4. Human Escalation Node
def escalation_node(state: SalesState):
    escalation_reason = state.get("escalation_reason", "High-value enterprise lead qualification required")
    
    human_decision = interrupt({
        "status": "Action Required",
        "message": f"The reason of escalation is: {escalation_reason}",
        "instructions": "Accept the enterprise decision or override it."
    })

    approval_msg = AIMessage(content=f"[Sales Director Review]: {human_decision.get('response', 'Approved')}")
    
    return {
        "messages": [approval_msg],  # FIXED: Wrapped inside list []
        "requires_human_escalation": False
    }


# 5. Conditional Logic: Agent -> Tools OR Evaluator
def should_continue_node(state: SalesState) -> Literal["tools", "lead_evaluator"]:
    messages = state.get("messages", [])
    if not messages:
        return "lead_evaluator"

    last_message = messages[-1]  # FIXED: Correct dictionary list slicing
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "lead_evaluator"


# 6. Conditional Logic: Evaluator -> Escalation OR End
def check_escaltion_node(state: SalesState) -> Literal["human_escalation", "__end__"]:
    if state.get("requires_human_escalation", False):
        return "human_escalation"
    return "__end__"