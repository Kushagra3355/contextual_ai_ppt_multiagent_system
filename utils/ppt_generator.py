from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from orchestrator.agent_state import ContentSlidesResponse
import os


def create_presentation(
    slides_data: ContentSlidesResponse, output_path: str, title: str = "Presentation"
) -> str:
    """Create PowerPoint presentation from ContentSlidesResponse data"""

    # Create presentation object
    prs = Presentation()

    # Add title slide
    title_slide_layout = prs.slide_layouts[0]  # Title slide layout
    slide = prs.slides.add_slide(title_slide_layout)
    title_placeholder = slide.shapes.title
    subtitle_placeholder = slide.placeholders[1]

    title_placeholder.text = title
    subtitle_placeholder.text = "Generated Presentation"

    # Add content slides
    for slide_data in slides_data.slides:
        # Use title and content layout
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)

        # Set slide title
        title_shape = slide.shapes.title
        title_shape.text = slide_data.title

        # Add content to body
        content_placeholder = slide.placeholders[1]
        text_frame = content_placeholder.text_frame
        text_frame.clear()

        for i, content_item in enumerate(slide_data.content):
            # Add paragraph for each content item
            if i == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()

            p.text = f"• {content_item.statement}"
            p.level = 0

            # Style based on status
            if content_item.status == "needs_review":
                # Make text italic for items needing review
                for run in p.runs:
                    run.font.italic = True
                    # Keep default color by not setting any color

            # Add design hint as a comment if available
            if content_item.design_hint:
                # Add design hint as smaller text
                hint_p = text_frame.add_paragraph()
                hint_p.text = f"    [{content_item.design_hint}]"
                hint_p.level = 1
                for run in hint_p.runs:
                    run.font.size = Pt(10)
                    run.font.italic = True

    # Save presentation
    prs.save(output_path)
    return output_path


def add_slide_with_bullet_points(
    prs: Presentation, title: str, bullet_points: list
) -> None:
    """Helper function to add a slide with bullet points"""
    slide_layout = prs.slide_layouts[1]  # Title and content layout
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.title
    title_shape.text = title

    content_placeholder = slide.placeholders[1]
    text_frame = content_placeholder.text_frame
    text_frame.clear()

    for i, point in enumerate(bullet_points):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        p.text = f"• {point}"
        p.level = 0
