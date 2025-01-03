from pydantic import BaseModel, Field


class CodeOrganizationParserEntity(BaseModel):
    business_code: str = Field(..., description="Use the latest code to obtain the complete business layer code")
    business_method_input_param: str = Field(..., description="Use the latest code to obtain the complete code of the input parameter class of the business class containing the @ TaskService annotation method")
    business_method_result_param: str = Field(...,
                              description="Use the latest code to obtain the @ TaskService annotation method and return the method's return parameter class")


    #使用最新的代码进行获取 除了业务代码,入参代码,返回参数代码的其他代码
    business_other_code: list[str] = Field(..., description="Use the latest code to obtain code other than business code, parameter code, and return parameter code. When there is no other code, return as empty")
    group_id: str = Field(..., description="GroupId in the root domain object")

    table_name: str = Field(..., description="table name in the root domain object")

    datasource: str = Field(..., description="datasource in the domain object")

    area_name: str = Field(..., description="area name in the domain object")

    task_component: str = Field(..., description="The value of the name attribute in @ TaskComponent in the business class")

    task_service: str = Field(..., description="The name attribute of @ TaskService annotation in business methods")

    maven_pom: str = Field(..., description="If spider coding experts suggest adding Maven dependencies in POM files, please return dependency information. If not, return empty. If a Maven dependency needs to be added, only add the content of the<dependency></dependency>structure")

