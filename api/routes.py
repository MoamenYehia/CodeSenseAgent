from fastapi import APIRouter , HTTPException 
from api.schemas import (ChatRequest,
                         ChatResponse,
                         EscalationApprovalResponse,
                         EscalationAprrovalRequest)

from services.agent_graph import app
from langgraph.types import Command
from langchain_core.messages import HumanMessage


router=APIRouter()

@router.post("/chat",response_model=ChatResponse)
async def chat_endpoint(payload:ChatRequest):
    config={"configurable":{"thread_id":payload.thread_id}}
    inputs={"messages":[HumanMessage(content=payload.message)]}
    try:
        for _ in app.stream(input=inputs,config=config,stream_mode="values"):
            pass
        current_state=app.get_state(config)

        if current_state.tasks[0].interrupts:
            interrupt_data=current_state.tasks[0].interrupts[0].value
            return ChatResponse(thread_id=payload.thread_id,
                                status="INTERRUPTED",
                                response="Your request involves custom Enterprise requirements (such as On-Premise deployment)."
                                          "Our Senior Sales Director has been notified to review and approve your request.",
                                interrupt_details=interrupt_data,)
        messages=current_state.values.get("messages",[])
        if not messages:
            raise HTTPException(status_code=500,
                                detail="Graph state returned no messages"
                                )
        last_message=messages[-1]
        return ChatResponse(thread_id=payload.thread_id,
                            status="Completed",
                            response=last_message.content)
    except Exception as e :
        raise HTTPException(status_code=500,detail=f"Error processing chat with id{payload.thread_id}")

@router.get("/pending_reviews/{thread_id}")
async def check_pending_reviews(thread_id:str):
    config={"configurable":{"thread_id:thread_id}"}}
    current_state=app.get_state(config)
    if current_state.tasks and current_state.tasks[0].interrupts:
        return {"thread_id":thread_id,
                "status":"Waiting for Approval",
                "interrupt_details":current_state.tasks[0].interrupts[0].value}
    return{"thread_id":thread_id,
           "status":"No need for Approval"}

@router.post("/approve_escalation",response_model=EscalationApprovalResponse)
async def approve_escalation_endpoint(payload:EscalationAprrovalRequest):
    config={"configurable":{"thread_id":payload.thread_id}}
    current_state=app.get_state(config)
    if not(current_state.tasks and current_state.tasks[0].interrupts):
        raise HTTPException(status_code=400,
                            detail=f"Thread '{payload.thread_id}' is not currently paused on an interrupt.")
    try:
        resume_command = Command(resume={"response": payload.decision})

        for _ in app.stream(resume_command, config=config, stream_mode="values"):
            pass
            final_state = app.get_state(config)
            final_messages = final_state.values.get("messages", [])
            last_msg = final_messages[-1] if final_messages else None
        
            return EscalationApprovalResponse(
                    thread_id=payload.thread_id,
                    status="RESUMED_AND_COMPLETED",
                    final_response=last_msg.content if last_msg else "Execution resumed successfully."
                )
        
    except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error resuming graph: {str(e)}")    