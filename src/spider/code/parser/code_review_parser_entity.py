from pydantic import BaseModel, Field


class CodeReviewParserEntity(BaseModel):
    is_improvement: bool = Field(...,
                                 description="Verify whether the code complies with the specifications, output False if it does not comply with the specifications")

    improvement_plan: str = Field(...,
                                  description="If improvement is needed, output improvement steps and plans, and try to answer in Chinese as much as possible")

    business_class_name: str = Field(..., description="generated business code class name")

    business_class_package: str = Field(..., description="The package name of the latest business code")

    function_input_parameters_package: str = Field(..., description="Method input package name in business code")

    business_class: str = Field(..., description="Use the latest code to obtain the business layer class code")

    service_package: str = Field(..., description="domainObjectServicePackage in the domain object")

    domainObject_package: str = Field(..., description="domainObjectPackage in the domain object")