import json
from pathlib import Path
from langchain_core.tools import tool

LEADS_FILE = Path("leads_crm.json")

@tool
def crm_lead_recorder(company_name: str, email: str, tier: str, summary: str) -> str:
    """
    Record qualified prospect details, matched tier, and business summary 
    into the CRM repository for sales tracking.

    Args:
        company_name: Name of the prospect's company.
        email: Contact email address.
        tier: Qualified tier (Solo Developer, Team, Enterprise).
        summary: Brief summary of user requirements and technical stack.
    """
    record = {
        "company": company_name,
        "email": email,
        "qualified_tier": tier,
        "notes": summary
    }

    leads = []
    if LEADS_FILE.exists():
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        except json.JSONDecodeError:
            leads = []

    leads.append(record)
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    return f"Lead for '{company_name}' ({email}) successfully logged in CRM under {tier} tier."