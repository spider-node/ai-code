from agentscope.parsers import MarkdownJsonDictParser

from src.spider.code.parser.TestCaseParserEntity import TestCaseParserEntity
from src.spider.code.parser.TestCaseSceneParserEntity import TestCaseSceneParserEntity
from src.spider.code.parser.code_organization_parser_entity import CodeOrganizationParserEntity
from src.spider.code.parser.code_review_parser_entity import CodeReviewParserEntity
from src.spider.code.parser.coder_class import CoderClass
from src.spider.code.parser.coder_standard_check import CoderStandardCheck


class OutParser:
    code_review_parser = MarkdownJsonDictParser(
        content_hint=CodeReviewParserEntity,
        required_keys=["improvement_plan", "is_improvement", "business_class_name", "business_class_package",
                       "function_input_parameters_package","business_class",
                       "service_package", "domainObject_package"],
        keys_to_memory=["improvement_plan", "is_improvement"],
        keys_to_content=["improvement_plan", "is_improvement", "business_class_name", "business_class_package",
                         "function_input_parameters_package", "business_class",
                         "service_package", "domainObject_package"],
    )

    code_organization_parser = MarkdownJsonDictParser(
        content_hint=CodeOrganizationParserEntity,
        required_keys=["business_code", "business_method_input_param", "group_id", "table_name", "area_name",
                       "datasource",
                       "task_component", "task_service"],
        keys_to_memory=["business_code", "business_method_input_param", "business_method_result_param", "group_id",
                        "table_name", "area_name",
                        "datasource", "task_component", "task_service", "maven_pom", "business_other_code"],
        keys_to_content=["business_code", "business_method_input_param", "business_method_result_param", "group_id",
                         "table_name", "area_name",
                         "datasource", "task_component", "task_service", "maven_pom", "business_other_code"],
    )

    test_case_param_and_sql = MarkdownJsonDictParser(content_hint=TestCaseParserEntity,
                                                     required_keys=["method_input_param", "case_sql"],
                                                     keys_to_memory=["method_input_param", "case_sql"],
                                                     keys_to_content=["method_input_param", "case_sql"], )

    test_case_scene = MarkdownJsonDictParser(content_hint=TestCaseSceneParserEntity,
                                             required_keys=["case_scenes"],
                                             keys_to_memory=["case_scenes"],
                                             keys_to_content=["case_scenes"], )

    class_code_name = MarkdownJsonDictParser(content_hint=CoderClass,
                                             required_keys=["business_class_name"],
                                             keys_to_memory=["business_class_name"],
                                             keys_to_content=["business_class_name"]
                                             )

    coder_standard_check = MarkdownJsonDictParser(content_hint=CoderStandardCheck,
                                                  required_keys=["code_standard_check"],
                                                  keys_to_memory=["code_standard_check", "correction_suggestions"],
                                                  keys_to_content=["code_standard_check", "correction_suggestions"] )
