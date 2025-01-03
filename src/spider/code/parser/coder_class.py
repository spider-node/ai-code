from pydantic import BaseModel, Field


class CoderClass(BaseModel):
    business_class_name: str = Field(..., description="generated business code class name")

    group_id: str = Field(..., description="GroupId in the root domain object")

    table_name: str = Field(..., description="table name in the root domain object")

