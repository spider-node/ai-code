from typing import List

from pydantic import BaseModel, Field


class TestCaseParserEntity(BaseModel):
    method_input_param: List[dict] = Field(...,
                                     description="Based on the latest code and testing scenarios, construct the execution parameters of domain functions for each scenario, as well as the expected results after execution, including whether there are any exceptions, case [{'inputParam':{},'resultIsException': true,'scene':'校验xxxx','sceneCode':''}],")

    case_sql: List[dict] = Field(...,
                           description="Before executing the test cases, it is necessary to prepare SQL to be [{sql:inserted into the MySQL database case insert into user (column1,column2) values (#{column1},#{column2}),param:{column1:1,column2:2},'sceneCode':''}] The content after values must strictly follow the style of values (# {column1}, # {column2}) and include fields with # {} inside  Determine whether SQL is required based on business logic needs")


