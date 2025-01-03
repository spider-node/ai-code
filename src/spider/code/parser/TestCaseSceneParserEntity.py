from typing import List

from pydantic import BaseModel, Field


class TestCaseSceneParserEntity(BaseModel):
    case_scenes: List[str] = Field(..., description="Test case scenarios generated based on the latest business code")
