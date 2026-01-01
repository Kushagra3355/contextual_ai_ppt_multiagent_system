from orchestrator.agent_state import PPTAgentState
from utils.ppt_generator import create_presentation
import os


def ExportAgent(state: PPTAgentState, output_dir: str = "outputs") -> PPTAgentState:
    """Export presentation to PowerPoint and draft text file"""

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Save draft
    with open("data/draft.txt", "w", encoding="utf-8") as f:
        f.write(f"PRESENTATION: {state.topic}\n{'=' * 80}\n\n")

        for i, slide in enumerate(state.validation_results, 1):
            f.write(f"SLIDE {i}: {slide.title}\n{'-' * 80}\n")

            for val in slide.validation:
                f.write(f"{val.point} ({val.status})\n")
                if val.reason:
                    f.write(f"   → {val.reason}\n")
            f.write("\n")

    # Export PowerPoint
    ppt_path = os.path.join(output_dir, "generated_ppt.pptx")
    create_presentation(state.validation_results, ppt_path, state.topic)

    print(f"✓ Exported: data/draft.txt and {ppt_path}")
    return state
