from typing import Optional , Any , Dict
from pydantic import BaseModel , Field

class ChatRequest(BaseModel):
    thread_id:str=Field(...,examples=["session 108"])
    message:str=Field(...,examples=["My lead email is something@uber and I need to know the plans"])

class ChatResponse(BaseModel):
    thread_id:str
    status:str=Field(...,
                     description="State of the turn: 'COMPLETED' (AI replied) or 'INTERRUPTED' (Waiting for human review).",
                     examples=["Completed"])
    response:Optional[str]=Field(
        None, 
        description="The AI's text response to display in the chat UI.")
    interrupt_details:Optional[Dict[str,Any]]=Field(None,description="why execution paused")

class EscalationAprrovalRequest(BaseModel):
    thread_id:str=Field(...,examples=["session 108"])
    decision:str=Field(...,
                       description="The human decision passed back to resume the interrupted graph.",
                       examples=["Approved for the enterprise plan"])

class EscalationApprovalResponse(BaseModel):
    thread_id:str
    status:str
    final_response:Optional[str]=None