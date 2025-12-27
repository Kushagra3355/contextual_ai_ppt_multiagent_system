from typing import Literal, Optional, Dict
from pydantic import BaseModel, Field


class content_agent_schema(BaseModel):  # content expansion agent
    slides: list[str] = Field(description="Give the outline of the ppt.")
    bullet_points: str = Field(description="Write the content for the slides")


class planner_agent_schema(BaseModel):  # outline generator agent
    slides: list[str] = Field(description="Give the outline of the ppt.")
    bullet_points: str = Field(description="Write the content for the slides")


class reviewer_agent_schema(BaseModel):  # qa agent
    slides: list[str] = Field(description="Give the outline of the ppt.")
    bullet_points: str = Field(description="Write the content for the slides")


# class format_optimizer_agent_schema(BaseModel):  ##optimizes the format
    # slides: list[str] = Field(description="Give the outline of the ppt.")
    # bullet_points: str = Field(description="Write the content for the slides")
