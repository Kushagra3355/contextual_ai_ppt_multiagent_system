from typing import Literal, Optional, Dict, List
from pydantic import BaseModel, Field

########################################################################################################


class Bulletslides(BaseModel):  # outline genarator
    title: str = Field(description="Give the outline title of the slides")
    bullet_points: List[str] = Field(
        description="Write the bullet points for the slides"
    )


class BulletslidesResponse(BaseModel):  # outline generatoragent
    slides: List[Bulletslides] = Field(
        description="Contains the tile and bullet points for each slide"
    )


########################################################################################################


class ContentExpansion(BaseModel):  # Content expansion agent
    title: str = Field(...,description="Title of each slide")
    detailed_points: List[str] = Field(
        description="Detailed points for each bullet point."
    )


########################################################################################################


class ValidationPoint(BaseModel):  # reviewer agent
    point: str = Field(..., description="Expanded statement")
    status: Literal["accurate", "needs_review"]
    reason: Optional[str] = Field(
        None, description="Why it needs review (required if status is needs_review)"
    )


class SlideValidation(BaseModel):  # reviewer agent
    title: str
    validation: List[ValidationPoint]


########################################################################################################


class SlideContentItem(BaseModel):  # format op agent
    statement: str = Field(
        ...,
        description="Final factual statement generated for the slide. Must be concise and verifiable.",
    )
    status: Literal["accurate", "needs_review"] = Field(
        ...,
        description="Fact-checking result for the statement. Use 'needs_review' if uncertainty exists.",
    )
    design_hint: Optional[str] = Field(
        None,
        description="Suggested minimal visual styling for this statement (icons, emphasis, layout).",
    )


class ContentSlide(BaseModel):  # format op agent
    title: str = Field(..., description="Title of the slide.")
    content: List[SlideContentItem] = Field(
        ..., description="List of validated content items for this slide."
    )


class ContentSlidesResponse(BaseModel):  # format op agent
    slides: List[ContentSlide] = Field(
        ...,
        description="Collection of slides with validated content ready for presentation.",
    )


########################################################################################################
