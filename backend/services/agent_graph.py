from langgraph.graph import START , END , StateGraph
from langgraph.checkpoint.memory import MemorySaver
from services.state import SalesState
from services.nodes import (sales_agent_node,
                            tools_node,
                            escalation_node,
                            lead_evaluator_node,
                            check_escaltion_node,
                            should_continue_node)

workflow=StateGraph(SalesState)

workflow.add_node("sales_agent_node",sales_agent_node)
workflow.add_node("tools",tools_node)
workflow.add_node("lead_evaluator_node",lead_evaluator_node)
workflow.add_node("escalation_node",escalation_node)

workflow.add_edge(START,"sales_agent_node")

workflow.add_conditional_edges("sales_agent_node",should_continue_node,
                               {"tools":"tools",
                                "lead_evaluator":"lead_evaluator_node"})

workflow.add_edge("tools","sales_agent_node")

workflow.add_conditional_edges("lead_evaluator_node",check_escaltion_node,
                               {"human_escalation":"escalation_node",
                                "__end__":END})

workflow.add_edge("escalation_node",END)

checkpointer=MemorySaver()
app=workflow.compile(checkpointer=checkpointer)