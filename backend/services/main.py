from langchain_core.messages import HumanMessage
from langgraph.types import Command
from services.agent_graph import app

def run_test():
    config = {"configurable": {"thread_id": "client_session_001"}}
    printed_ids = set()

    def process_stream(input_data):
        """Streams all node outputs and prints Tool Results and AI Responses."""
        for event in app.stream(input_data, config=config, stream_mode="values"):
            for msg in event.get("messages", []):
                if msg.id not in printed_ids:
                    printed_ids.add(msg.id)

                    # 1. User Input
                    if msg.type == "human":
                        print(f"\n[HUMAN]: {msg.content}")

                    # 2. AI Tool Call Request
                    elif msg.type == "ai" and hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            print(f"\n[AI TOOL CALL]: Calling '{tool_call.get('name')}' with args {tool_call.get('args')}")

                    # 3. Executed Tool Output
                    elif msg.type == "tool":
                        snippet = msg.content if len(msg.content) < 200 else msg.content[:200] + "..."
                        print(f"\n[TOOL RESULT ({msg.name})]:\n{snippet}")

                    # 4. Final Text Answer from LLM
                    elif msg.type == "ai" and msg.content:
                        print(f"\n[AI RESPONSE]:\n{msg.content}")

    # --- TURN 1: Initial Product Inquiry ---
    print("\n==================================================")
    print("--- Turn 1: Initial Inquiry ---")
    print("==================================================")
    process_stream({"messages": [HumanMessage(content="Hi! What plans do you offer for CodeSense AI?")]})

    # --- TURN 2: Enterprise Contact & Requirements ---
    print("\n==================================================")
    print("--- Turn 2: Enterprise Lead & On-Premise Requirement ---")
    print("==================================================")
    process_stream({"messages": [HumanMessage(content="My email is lead@stripe.com. We are looking for an on-premise deployment.")]})

    # --- ADVANCE GRAPH INTO ESCALATION NODE ---
    # Passing None lets the graph execute the pending conditional edge into human_escalation_node
    process_stream(None)

    # --- CHECK INTERRUPT STATE ---
    print("\n==================================================")
    print("--- Checking Interrupt & State Verification ---")
    print("==================================================")

    current_state = app.get_state(config)

    # Verify if graph is paused at human_escalation_node
    if current_state.tasks and current_state.tasks[0].interrupts:
        print("\n[SUCCESS]: Workflow successfully paused via interrupt()!")
        interrupt_payload = current_state.tasks[0].interrupts[0].value
        print(f"Interrupt Details: {interrupt_payload}")

        # --- SIMULATE SALES DIRECTOR APPROVAL ---
        print("\n--------------------------------------------------")
        print("--- Simulating Sales Director Approval (Resume) ---")
        print("--------------------------------------------------")

        resume_command = Command(
            resume={"response": "Approved Enterprise On-Premise request. Forwarded to Sales Director."}
        )
        process_stream(resume_command)
        print("\n[SUCCESS]: Workflow resumed and finished successfully!")
    else:
        print(f"\n[DEBUG]: State next node: {current_state.next}")
        print(f"Escalation Flag: {current_state.values.get('requires_human_escalation')}")

if __name__ == "__main__":
    run_test()