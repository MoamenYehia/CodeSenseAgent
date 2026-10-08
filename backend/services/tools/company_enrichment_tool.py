import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def company_enrichment_tool(email_or_domain: str) -> str:
    """
    Look up factual company intelligence (company name, employee count, industry, country)
    using the client's work email address or domain name.

    Args:
        email_or_domain: The prospect's email address or company website domain.
    """
    text = email_or_domain.lower().strip()
    domain = text.split("@")[-1] if "@" in text else text

    free_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    if domain in free_domains:
        return f"Domain: {domain} is a public/personal mailbox. Organization: Individual/Unknown."

    api_key = os.getenv("ABSTRACT_API_KEY")
    if not api_key:
        return "Error: ABSTRACT_API_KEY is missing."

    url=f"https://companyenrichment.abstractapi.com/v2?api_key={api_key}&domain={domain}"

    try:
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            return f"Failed to retrieve data for {domain} (HTTP {response.status_code})."

        data = response.json()
        if not data or not data.get("company_name"):
            return f"No public corporate records found for domain: {domain}."

        return (
            f"Company: {data.get('company_name')}\n"
            f"Industry: {data.get('industry', 'N/A')}\n"
            f"Country: {data.get('country', 'N/A')}\n"
            f"Total Employees: {data.get('employee_count', 'Unknown')}\n"
            f"Description: {data.get('description', 'No description available.')}"
        )

    except requests.exceptions.RequestException as e:
        return f"Enrichment service unreachable: {str(e)}"


if __name__ =="__main__":
    domain_query="moamenyehia@posthog.com"
    personal_query="yehiamo@gmail.com"
    results=company_enrichment_tool.invoke(domain_query)
    print(results)    