from langgraph.graph import StateGraph, END
from typing import Dict, Any
from agents.outline_generator_agent import OutlineAgent
from agents.content_expansion_agent import ContentExpansionAgent
from agents.reviewer_agent import ReviewerAgent
from agents.format_optimizer_agent import FormatOptimizerAgent
from agents.export_agent import ExportAgent


def create_ppt_graph() -> StateGraph:
    """Create the PowerPoint generation workflow graph"""

    # Initialize the graph
    workflow = StateGraph(Dict[str, Any])

    # Add nodes for each agent
    workflow.add_node("outline", OutlineAgent)
    workflow.add_node("expand", ContentExpansionAgent)
    workflow.add_node("review", ReviewerAgent)
    workflow.add_node("optimize", FormatOptimizerAgent)
    workflow.add_node("export", ExportAgent)

    # Define the workflow edges
    workflow.add_edge("outline", "expand")
    workflow.add_edge("expand", "review")
    workflow.add_edge("review", "optimize")
    workflow.add_edge("optimize", "export")
    workflow.add_edge("export", END)

    # Set entry point
    workflow.set_entry_point("outline")

    return workflow


def run_ppt_generation(topic: str, context: str = "") -> Dict[str, Any]:
    """Execute the complete PowerPoint generation pipeline"""

    # Create the workflow
    app = create_ppt_graph().compile()

    # Initial state
    initial_state = {
        "topic": topic,
        "context": context,
        "outline": None,
        "expanded_content": None,
        "validated_content": None,
        "final_slides": None,
        "export_status": None,
        "output_file": None,
    }

    # Run the workflow
    result = app.invoke(initial_state)

    return result


def get_workflow_status(state: Dict[str, Any]) -> str:
    """Get current workflow status for monitoring"""
    if state.get("export_status") == "success":
        return f"✅ Complete - File: {state.get('filename', 'N/A')}"
    elif state.get("final_slides"):
        return "🔄 Exporting presentation..."
    elif state.get("validated_content"):
        return "🔄 Optimizing format..."
    elif state.get("expanded_content"):
        return "🔄 Reviewing content..."
    elif state.get("outline"):
        return "🔄 Expanding content..."
    else:
        return "🔄 Creating outline..."
