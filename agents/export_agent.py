from orchestrator.agent_state import ContentSlidesResponse
from utils.ppt_generator import create_presentation
from datetime import datetime
import os


def ExportAgent(state: dict) -> dict:
    """Export final slides to PowerPoint presentation"""
    final_slides = state.get("final_slides")
    topic = state.get("topic", "Presentation")

    try:
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{topic.replace(' ', '_')}_{timestamp}.pptx"
        output_path = os.path.join("output", filename)

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

        # Create presentation
        file_path = create_presentation(final_slides, output_path, title=topic)

        return {
            "export_status": "success",
            "output_file": file_path,
            "filename": filename,
        }

    except Exception as e:
        return {"export_status": "failed", "error": str(e)}
