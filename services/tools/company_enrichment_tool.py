from langchain.tools import tool
from services.retrieving import retrieving

retrieving_function=retrieving()

@tool
def company_enrichment_tool(query:str)->str:
    """
Search official CodeSense AI documentation, pricing tiers, and platform features.
Use this tool whenever the user asks about plans, subscription costs, GitHub/GitLab integrations, or company policies.

Args:
    query: The search keywords or user question regarding CodeSense AI.
"""
    response=retrieving_function.invoke(query)
    if not response:
        raise ValueError ("there is not realted polices")
    formated_docs=[]
    for i , doc in enumerate(response):
        source=doc.metadata.get("source","Product_Catalog")
        formated_docs.append(f"---Policy Excerpt {i+1} ({source})---\n{doc.page_content.strip()}")

    return "\n\n".join(formated_docs)


#Test_function
if __name__ == "__main__":
    print("Tool Name:", company_enrichment_tool.name)
    print("Tool Description:\n", company_enrichment_tool.description)
    print("-" * 50)

    test_query = "What is the Refund & Cancellation Policy"
    print(f"Testing Query: '{test_query}'\n")

    result = company_enrichment_tool.invoke({"query": test_query})

    print("--- Tool Output ---")
    print(result)
    