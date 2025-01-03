from pydantic import BaseModel, Field


class CoderStandardCheck(BaseModel):
    code_standard_check: bool = Field(...,description="code standard check Return True if satisfied, return False if not satisfied")

    correction_suggestions: str = Field(..., description="If not met, please provide feedback on the output of spider code management")


