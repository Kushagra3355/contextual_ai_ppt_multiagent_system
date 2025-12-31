from langgraph.graph import StateGraph, END
from orchestrator.agent_state import PPTAgentState
from agents.outline_generator_agent import OutlineAgent
from agents.content_expansion_agent import ContentExpansionAgent
from agents.reviewer_agent import ReviewerAgent
from agents.export_agent import ExportAgent


def create_ppt_graph() -> StateGraph:
    """Create the PowerPoint generation workflow graph"""
    workflow = StateGraph(PPTAgentState)

    # Add agent nodes
    workflow.add_node("outline", OutlineAgent)
    workflow.add_node("expand", ContentExpansionAgent)
    workflow.add_node("review", ReviewerAgent)
    workflow.add_node("export", ExportAgent)

    # Define workflow: Outline → Expand → Review → Export
    workflow.add_edge("outline", "expand")
    workflow.add_edge("expand", "review")
    workflow.add_edge("review", "export")
    workflow.add_edge("export", END)

    workflow.set_entry_point("outline")
    return workflow


def run_ppt_generation(topic: str, slides: int = 7, context: str = "") -> PPTAgentState:
    """Execute the complete PowerPoint generation pipeline"""
    app = create_ppt_graph().compile()

    initial_state = PPTAgentState(topic=topic, slides=slides, context=context)

    result = app.invoke(initial_state)
    return result


def get_workflow_status(state: PPTAgentState) -> str:
    """Get current workflow status"""
    if state.validation_results:
        return "✓ Complete - Exported to output folder"
    elif state.expanded_content:
        return "Reviewing content..."
    elif state.outline:
        return "Expanding content..."
    else:
        return "Creating outline..."
