from typing import Optional , Sequence ,Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage 
from langgraph.graph.message import add_messages

class SalesState(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]

    company_name:Optional[str]
    lead_email:Optional[str]
    qualified_tier:Optional[str] # Solo , Team , Enterprise

    requires_human_escalation:bool
    escalation_reason:Optional[str]