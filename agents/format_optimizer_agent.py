from orchestrator.agent_state import (
    SlideContentItem,
    ContentSlide,
    ContentSlidesResponse,
    SlideValidation,
)
from app.dependencies import llm as get_llm
from typing import List


def FormatOptimizerAgent(state: dict) -> dict:
    """Optimize content format for presentation delivery"""
    validated_content = state.get("validated_content", [])

    llm = get_llm()
    final_slides = []

    for slide_validation in validated_content:
        if not isinstance(slide_validation, SlideValidation):
            continue

        content_items = []

        for validation in slide_validation.validation:
            # Generate design hint
            prompt = f"""
Suggest a minimal design hint for this statement:
"{validation.point}"

Provide a brief styling suggestion (icon, emphasis, layout) in 3-5 words.
"""

            response = llm.invoke(prompt)
            design_hint = response.content.strip()[:50]  # Keep it short

            content_items.append(
                SlideContentItem(
                    statement=validation.point,
                    status=validation.status,
                    design_hint=design_hint,
                )
            )

        final_slides.append(
            ContentSlide(title=slide_validation.title, content=content_items)
        )

    result = ContentSlidesResponse(slides=final_slides)
    return {"final_slides": result}
