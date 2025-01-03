from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict, List, Any

from langchain.agents import AgentExecutor
from langgraph.graph.graph import CompiledGraph

from agentscope.agents import DialogAgent, ReActAgent
from agentscope.msghub import MsgHubManager
from src.spider.code.agent.spider_dict_dialog_agent import SpiderDictDialogAgent
from src.spider.code.agent.spider_user_agent import SpiderUserAgent
from src.spider.code.test import TestScene


class CodeContext(TypedDict):
    #
    input: str
    # 生成代码的步骤
    steps: str
    # 业务层代码
    business_code: str
    # 最新的输出代码
    code: str
    # 参数代码
    param_code: str
    # 出参代码
    result_code: str
    # pom中的 groupId
    group_id: str
    # 领域的表名称
    table_name: str
    # 数据源名称
    datasource: str
    maven_pom: str
    # 领域对象 java
    domain_object: str
    # java 业务开发
    senior_java_programming_expert: DialogAgent
    # 领域助手
    domain_assistant_agent: DialogAgent
    # java 代码check
    code_review: SpiderDictDialogAgent
    # 代码整理
    code_organization: SpiderDictDialogAgent
    # spider-系统角色
    system_agent: SpiderUserAgent
    # 代码优化
    code_optimization_expert: DialogAgent

    code_assistant: SpiderDictDialogAgent

    technical_proposal: DialogAgent

    java_expert: DialogAgent

    # 测试数据准备
    test_init_data_agent: SpiderDictDialogAgent

    function_parameters_package_name: str

    # 测试场景用例输出
    test_case_scene_agent: SpiderDictDialogAgent

    java_code_specification_validation: SpiderDictDialogAgent

    flow_data_agent: DialogAgent

    sql_agent: CompiledGraph

    # 本次中的代码审查次数
    code_review_count: int
    # 是否需要优化
    meet_the_standards: bool

    # 当前角色
    current_role: str
    # 流程结束
    end: bool
    # 具体领域
    domain: str
    # 子域信息
    sub_domain: str

    domain_info: List[dict]
    # 是否支持编码
    support_encod: bool

    # 组件名称
    task_component: str

    # 组件的功能名称
    task_service: str

    # 编译成功或者失败
    compile_status: str

    # 是否进行过优化
    is_it_optimized: bool

    # 测试用例
    test_scenes: List[TestScene]

    business_requirements: List[str]

    task_id: str

    domain_base_id: list[int]

    domain_function_version_id: str

    # 开启测试的id
    teat_task_id: int

    business_class_code: str

    business_code_markdown: str

    business_input_class_code: str

    business_input_class_code_markdown: str

    business_output_class_code: str

    business_output_class_code_markdown: str

    table_name: str

    group_id: str

    business_other_code: list[str]

    code_standard_check: bool

    correction_suggestions: str

    import_error: str

    code_error_info: dict

    compile_error_count: int

    executor: ThreadPoolExecutor

    spider_url: str

    flow_data_info: dict

    flow_data_desc: str

    need_data_flow: bool

    code_organization_count: int
    code_organization_status: bool




