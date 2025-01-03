from pydantic import Field


class TestCaseSceneParser:
    method_input_param: dict = Field(...,
                                     description="Based on the latest code and test scenarios, construct execution parameters for domain functions for each scenario")

    case_sql: dict = Field(...,
                           description="Before executing the test cases, it is necessary to prepare SQL to be inserted into the MySQL database case insert into user column1,column2 values (#{column1},#{column2})")

    case_sql_param: dict = Field(...,
                                 description="SQL prepared data, containing only data case [{column1:123,column2:456}]")
