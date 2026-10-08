from langchain_core.tools import tool
import uuid

@tool
def calendar_booking_tool(email: str, preferred_slot: str, plan_name: str) -> str:
    """
    Schedule a live technical product demo or sales call once the client agrees 
    on a suitable plan and provides their preferred date/time.

    Args:
        email: The prospect's email address.
        preferred_slot: The requested date and time (e.g., 'Tomorrow at 3 PM UTC' or '2026-10-15 14:00').
        plan_name: The CodeSense AI plan under discussion (Solo, Team, or Enterprise).
    """
    booking_id = str(uuid.uuid4())[:8]
    meeting_link = f"https://meet.google.com/cds-{booking_id}"
    
    return (
        f"Demo Booking Confirmed!\n"
        f"- Booking ID: {booking_id}\n"
        f"- Attendee: {email}\n"
        f"- Scheduled Slot: {preferred_slot}\n"
        f"- Target Plan: {plan_name}\n"
        f"- Meeting Link: {meeting_link}\n"
        f"- Status: Calendar invite dispatched."
    )