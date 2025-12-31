from typing import Literal, Optional, List
from pydantic import BaseModel, Field


class Bulletslides(BaseModel):
    """Outline slide with title and bullet points"""

    title: str = Field(description="Slide title")
    bullet_points: List[str] = Field(description="Bullet points for the slide")


class ContentExpansion(BaseModel):
    """Expanded slide content"""

    title: str = Field(description="Slide title")
    detailed_points: List[str] = Field(description="Detailed content points")


class ValidationPoint(BaseModel):
    """Validation result for a content point"""

    point: str = Field(description="Content statement")
    status: Literal["accurate", "needs_review"]
    reason: Optional[str] = Field(None, description="Reason if needs review")


class SlideValidation(BaseModel):
    """Validation results for a slide"""

    title: str
    validation: List[ValidationPoint]


class BulletslidesResponse(BaseModel):
    """Outline generator response"""

    slides: List[Bulletslides] = Field(description="List of outline slides")


class ExpandedContentResponse(BaseModel):
    """Content expansion response"""

    slides: List[ContentExpansion] = Field(description="List of expanded slides")


class PPTAgentState(BaseModel):
    """Unified Pydantic state for all PPT generation agents"""

    # Input (required)
    topic: str = Field(description="PPT topic")
    slides: int = Field(default=7, description="Number of slides to generate")

    # Outline Generator output
    outline: Optional[BulletslidesResponse] = Field(
        default=None, description="Generated outline"
    )

    # Content Expansion output
    expanded_content: Optional[List[ContentExpansion]] = Field(
        default=None, description="Expanded content"
    )

    # Reviewer output
    validation_results: Optional[List[SlideValidation]] = Field(
        default=None, description="Validation results"
    )

    # Metadata
    context: Optional[str] = Field(default=None, description="Additional context")
