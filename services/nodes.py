from services.tools.calender_booking_tool import calendar_booking_tool
from services.tools.company_enrichment_tool import company_enrichment_tool
from services.tools.crm_lead_recorder import crm_lead_recorder
from services.tools.rag_tool import rag_tool
from langgraph.prebuilt import ToolNode
from services.state import SalesState
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage , AIMessage
from langgraph.types import interrupt
from typing import Literal

load_dotenv()





sales_tools=[calendar_booking_tool,company_enrichment_tool,crm_lead_recorder,rag_tool]

tools_node=ToolNode(sales_tools)


def sales_agent(state:SalesState, config=RunnableConfig):
    llm=ChatGroq(model="qwen/qwen3.8-27b",api_key=os.getenv("GROQ_API_KEY"),temperature=0.3)
    llm_with_tools=llm.bind_tools(sales_tools)

    system_prompt=SystemMessage(content=("You are CodeSense AI's top B2B Senior Sales Engineer.\n"
        "Your objective is to qualify leads, match them to the correct pricing tier (Solo, Team, Enterprise), "
        "and guide them toward booking a demo or recording their lead in the CRM.\n\n"
        "Execution Rules:\n"
        "1. Always consult `rag_product_docs` for authoritative pricing, features, and policy rules.\n"
        "2. When a user provides a work email or company domain, invoke `company_enrichment_tool` to check headcount.\n"
        "3. Match the user to Team Tier (2-25 devs) or Enterprise Tier (>25 devs or compliance/on-prem needs).\n"
        "4. Be professional, concise, and helpful."))

    messages=system_prompt+list[state["messages"]]
    response=llm_with_tools.invoke(messages)
    return {"messages":[response]}

def lead_evaluator_node(state:SalesState):
    messages=state.get("messages",[])
    if not messages:
        return{}
    last_message=messages[-1]
    content=last_message.content.lower() if isinstance(last_message,AIMessage) else ""
    requires_human_escalation=False
    escalation_reason=None
    if "enterprise" in content and ("custom contract" in content or "escalat" in content or "sales director" in content):
        requires_human_escalation = True
        escalation_reason = "High-value Enterprise deal identified requiring Sales Director custom approval."
    elif "on-premise" in content or "air-gapped" in content or "soc2 report" in content:
        requires_human_escalation = True
        escalation_reason = "Custom compliance or On-Premise deployment requested."

    return{"requires_human_escalation":requires_human_escalation,
           "escalation_reason":escalation_reason
           }

def escalation_node(state:SalesState):
    escalation_reason=state.get("escalation_reason","High-value enterprise lead qualification required")  
    human_decision=interrupt({"status":"Action Required",
                              "message":f"The reason of escalation is {escalation_reason}",
                              "instructions":"Accept the enterpise decision or override it"}
                              ) 

    approval_msg=AIMessage(content=f"[Sales Director review]:{human_decision.get("response","Approved")}")

    return {"messages":approval_msg,
            "requires_human_escalation":False}

def should_continue(state:SalesState)->Literal["tools","lead_evaluator"]:
    last_message=state.get("messages"[-1])
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        return "tools"
    return "lead_evaluator"

def check_escaltion(state:SalesState)->Literal["human_escalation","__end__"]:
    if state.get("requires_human_escalation",False):
        return "human_escalation"
    return "__end__"
    
