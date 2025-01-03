import json
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Literal, Any
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from agentscope.agents import UserAgent, DialogAgent, AgentBase
from agentscope.message import Msg
from src.spider.code.agent.spider_dict_dialog_agent import SpiderDictDialogAgent
from src.spider.code.agent.spider_user_agent import SpiderUserAgent
from src.spider.code.chat.use_spider_illustrate import system_prompt, system_miss_role
from src.spider.code.config.agent_config import senior_java_programming_expert_config, \
    user_agent_config, code_review_agent_config, code_organization_agent_config, \
    system_agent_config, domain_assistant_agent_config, logical_technical_solution_config, code_optimization, \
    test_engineer, test_case_scene_engineer, init_test_data, code_assistant, java_expert, flow_data_agent
from src.spider.code.config.out_parser import OutParser
from src.spider.code.context.code_context import CodeContext
from src.spider.code.test.TestScene import TestScene
from src.spider.code.tool.CodeCase import business_code, input_param_code, out_put_param_code
from src.spider.code.tool.CodeTool import deploy_code_to_application, \
    check_package_business_code_v1, generate_package_domain_prefix, \
    generate_package, notify_task_step
from src.spider.code.tool.TestDataStorage import run_case
from src.spider.code.tool.domain_tool import query_domain_rag, query_domain_info_v1
from src.spider.code.util.area_util import query_current_role
from src.spider.code.util.code_util import java_to_markdown_code_block


# 输出代码的实现逻辑
def logic_programming(state: CodeContext):
    technical_proposal = state['technical_proposal']
    technical_proposal()


def senior_java_programming_expert_node(state: CodeContext):
    senior_java_programming_expert = state["senior_java_programming_expert"]
    x = senior_java_programming_expert()
    code_review = state["code_review"]
    code_organization_agent = state["code_organization"]
    test_init_data_agent = state["test_init_data_agent"]
    test_case_scene_agent = state["test_case_scene_agent"]
    agents = [code_review, test_init_data_agent, test_case_scene_agent, code_organization_agent]
    # 通知给 code_review 让他去进行

    notify_msg_to_memory_msg(agents, msg=x)
    executor = state['executor']
    spider_url = state['spider_url']
    task_id = state['task_id']
    executor.submit(notify_task_step, spider_url, "CODER", task_id, "")
    return {
        "code": x.content,
    }


# 优化代码逻辑
def code_optimization_execute(state: CodeContext):
    code_optimization_expert = state["code_optimization_expert"]
    code_optimization_expert()
    return {
        "is_it_optimized": False
    }


# 领域助手
def domain_assistant_agent_node(state: CodeContext):
    domain = state["domain"]
    input = state["input"]
    system_agent = state["system_agent"]
    domain_assistant_agent = state["domain_assistant_agent"]
    if domain == "" or domain is None:
        result = query_domain_rag(input)
        system_agent.speak(str(result))
    else:
        # 领域助手进行分析
        domain_assistant_agent()


# 代码规范审查的步骤
def code_review_node(state: CodeContext):
    code_review = state["code_review"]
    code_review_count = state["code_review_count"]
    non_conformance_specification = []
    executor = state['executor']
    spider_url = state['spider_url']
    task_id = state['task_id']
    executor.submit(notify_task_step, spider_url, "CHECK", task_id, "")
    # 尝试执行的代码块
    try:
        x = code_review()
        context_json = json.dumps(x.content, ensure_ascii=False)
        print("code_review_node 源码为 {}", context_json)
        # 校验是否包含@sofa的注解
        review_result = json.loads(context_json)
        improvement_plan = review_result['improvement_plan']
        business_class_name = review_result['business_class_name']
        business_class_package = review_result['business_class_package']
        business_class = review_result['business_class']
        table_name = state['table_name']
        group_id = state['group_id']
        function_input_parameters_package = state['function_parameters_package_name']

        check_result = check_package_business_code_v1(business_class_name=business_class_name,
                                                      business_class_package=business_class_package,
                                                      business_class=business_class,
                                                      table_name=table_name, group_id=group_id,
                                                      function_input_parameters_package=function_input_parameters_package)
        non_conformance_specification = check_result['improve']
        meet_the_standards = check_result['is_improvement']
        if len(non_conformance_specification) != 0:
            meet_the_standards = False
            non_conformance_specification.append(improvement_plan)

            non_conformance_specification.append(
                "重点，修改提示错误的内容，不用去额外修改其他内容，修改后输出完整的入参，出参，业务方法的逻辑代码")
            senior_java_programming_expert = state["senior_java_programming_expert"]
            agents = [senior_java_programming_expert]
            notify_msg_to_memory_any(agents=agents, msg=non_conformance_specification)
            code_review.speak(str(non_conformance_specification))
            # 代码审查异常
            executor.submit(notify_task_step, spider_url, "CHECK", task_id, str(non_conformance_specification)).result()
    except Exception as e:
        print("异常信息为", e)
        traceback.print_exc()
        meet_the_standards = False
        pass
    print("校验结果为", non_conformance_specification)
    return {
        "code_review_count": code_review_count + 1,
        "meet_the_standards": meet_the_standards
    }


def check_organized_code(state: CodeContext):
    java_code_specification_validations = state["java_code_specification_validation"]
    x = java_code_specification_validations()
    context_json = json.dumps(x.content, ensure_ascii=False)
    review_result = json.loads(context_json)
    code_standard_check = review_result.get("code_standard_check")
    correction_suggestions = review_result.get("correction_suggestions")

    return {
        "code_standard_check": code_standard_check,
        "correction_suggestions": correction_suggestions
    }


# 代码整理
def code_organization_node(state: CodeContext):
    code_organization_agent = state["code_organization"]
    code_organization_count = state["code_organization_count"]
    executor = state['executor']
    spider_url = state['spider_url']
    task_id = state['task_id']
    # arrangement
    executor.submit(notify_task_step, spider_url, "CODER_ARRANGEMENT", task_id, "")
    code_organization_status = False
    try:

        review_result = code_organization_agent_run(code_organization_agent, msg="")
        business_code_markdown = java_to_markdown_code_block(review_result.get("business_code"))
        import_error = check_import_section(business_code_markdown)
        if import_error is not None:
            msg = "During the process of outputting business_comde, please pay attention to the previous erroneous export" + import_error + "输出业务代码过程中,请修正该细节"
            review_result = code_organization_agent_run(code_organization_agent, msg=msg)
            business_code_markdown = java_to_markdown_code_block(review_result.get("business_code"))
            import_error = check_import_section(business_code_markdown)
            if import_error is not None:
                print("----整理代码--出现连续两次不正确")
                # 抛异常结束程序
                executor.submit(notify_task_step, spider_url, "CODER_ARRANGEMENT", task_id,
                                "整理代码--出现连续两次不正确")
                code_organization_status = True
                code_organization_count = code_organization_count + 1
        param_code_markdown = java_to_markdown_code_block(review_result.get("business_method_input_param"))
        result_code = review_result.get("business_method_result_param")
        business_other_code = review_result.get("business_other_code")
        print("额外的代码信息为", business_other_code)
        code_organization_agent.speak("我们将整理出业务层代码")
        code_organization_agent.speak(business_code_markdown)
        code_organization_agent.speak("我们将整理方法的入参代码")
        code_organization_agent.speak(param_code_markdown)

        result_code_markdown = ""
        if result_code is not None:
            code_organization_agent.speak("我们将整理方法的返回参数代码")
            result_code_markdown = java_to_markdown_code_block(result_code)
            code_organization_agent.speak(result_code_markdown)
        return {
            "business_code": review_result.get("business_code"),
            "param_code": review_result.get("business_method_input_param"),
            "result_code": review_result.get("business_method_result_param"),
            "datasource": review_result.get("datasource"),
            "area_name": review_result.get("area_name"),
            "task_component": review_result.get("task_component"),
            "task_service": review_result.get("task_service"),
            "maven_pom": review_result.get("maven_pom"),
            "business_other_code": review_result.get("business_other_code"),
            "import_error": import_error,
            "business_code_markdown": business_code_markdown,
            "business_input_class_code_markdown": param_code_markdown,
            "business_output_class_code_markdown": result_code_markdown,
            "code_organization_status": code_organization_status,
        }
    except Exception as e:
        code_organization_agent.speak(str(e))
        code_organization_count = code_organization_count + 1
        code_organization_status = True
        return {
            "code_organization_count": code_organization_count,
            "code_organization_status": code_organization_status
        }


def check_code_organization(state: CodeContext) -> Literal[
    "compile_code", "__end__", "code_organization_node"]:
    code_organization_status = state["code_organization_status"]
    code_organization_count = state["code_organization_count"]
    if code_organization_status and code_organization_count >= 3:
        return "__end__"
    elif code_organization_status:
        return "code_organization_node"
    else:
        return "compile_code"


def code_organization_agent_run(code_organization_agent: SpiderDictDialogAgent, msg: str) -> json:
    if msg == "":
        x = code_organization_agent()
    else:
        x = code_organization_agent(Msg(content=msg, name="Moderator", role="assistant"))
    context_json = json.dumps(x.content, ensure_ascii=False)
    return json.loads(context_json)


def check_import_section(java_code) -> str:
    lines = java_code.splitlines()
    in_import_section = False  # 标记是否在import代码块中
    missing_imports = []
    for line in lines:
        stripped_line = line.strip()

        # 如果遇到了 package 声明，则开始进入 import 区域
        if stripped_line.startswith('package'):
            in_import_section = True
            continue

        # 如果遇到了 public class 定义，则结束 import 区域
        if 'public class' in stripped_line:
            break

        # 在 import 区域中检查是否有缺少 'import' 关键字的导入语句
        if in_import_section and stripped_line and not stripped_line.startswith(('import', '@')):
            if stripped_line.endswith(';'):
                missing_imports.append(line)

    if missing_imports:
        print("Warning: Found potential import statements without 'import' keyword:")
        # 把missing_imports 转换成字符串 进行return
        return "\n".join(missing_imports)
    else:
        return None


def create_business_class_info(state: CodeContext):
    code_assistant = state.get("code_assistant")
    x = code_assistant()
    context_json = json.dumps(x.content, ensure_ascii=False)
    review_result = json.loads(context_json)
    table_name = state['table_name']
    group_id = state['group_id']
    business_class_name = review_result.get("business_class_name")
    business_base_path = generate_package(table_name=table_name, group_id=group_id,
                                          business_code_class_name=business_class_name)

    business_code_class_name_new = business_base_path + ".spider.service"
    function_parameters_package_new = business_base_path + ".spider.data"

    business_code_class_infos = "Please use the name of the business class " + business_class_name + " Business class, please import parameters and export parameter packages " + function_parameters_package_new + "The package name of the input and output parameter classes" + function_parameters_package_new + "Package names outside of input, output, and business class" + function_parameters_package_new + " Package for this business class " + business_code_class_name_new
    senior_java_programming_expert = state['senior_java_programming_expert']
    code_review = state['code_review']
    java_experts = state['java_expert']
    agents = [senior_java_programming_expert, code_review, java_experts]
    notify_msg_to_memory_any(msg=business_code_class_infos, agents=agents)
    code_assistant.speak(business_code_class_infos)
    return {
        "function_parameters_package_name": function_parameters_package_new
    }


def check_role(state: CodeContext):
    current_role = state["current_role"]
    end = False
    if current_role == "" or current_role is None:
        system_agent = state['system_agent']
        system_agent.speak(system_miss_role)
        end = True
    # 通知群内成员-
    return {
        "end": end
    }


def compile_code(state: CodeContext):
    executor = state['executor']
    # arrangement

    code_error_info = {}
    business_code = state["business_code"]
    param_code = state["param_code"]
    result_code = state["result_code"]
    table_name = state["table_name"]
    datasource = state["datasource"]
    task_component = state["task_component"]
    task_service = state["task_service"]
    compile_status = "suss"
    domain_base_id = state["domain_base_id"]
    task_id = state["task_id"]
    domain_function_version_id = state["domain_function_version_id"]
    maven_pom = state["maven_pom"]
    spider_url = state["spider_url"]
    try:
        response = deploy_code_to_application(business_code=business_code, param_code=param_code,
                                              result_code=result_code,
                                              table_name=table_name, datasource=datasource,
                                              task_component=task_component, task_service=task_service,
                                              domain_base_id=domain_base_id, task_id=task_id,
                                              domain_function_version_id=domain_function_version_id,
                                              maven_pom=maven_pom,
                                              spider_url=spider_url)
        print("编译代码的返回值", response)
        system_agent = state["system_agent"]
        code = response['code']
        speak_msg = response['msg']

        if code == 400:
            compile_status = "fail"
            # 有数据
            system_agent.speak("部署失败部署返回内容" + speak_msg)
        elif code == 0:
            data = response['data']
            if data:
                errorStackTrace = data['errorStackTrace']
                if errorStackTrace:
                    compile_status = "fail"
                    notify_error = "部署报错" + errorStackTrace
                    # 通知具体的步骤
                    executor.submit(notify_task_step, spider_url, "COMPILE_ERROR", task_id, errorStackTrace)
                    # 告知一些细节信息给 java_expert
                    code_error_info = {
                        "business_code_markdown": state["business_code_markdown"],
                        "business_input_class_code_markdown": state["business_input_class_code_markdown"],
                        "business_output_class_code_markdown": state["business_output_class_code_markdown"],
                        "compile_error_stack_trace": errorStackTrace
                    }
                    system_agent.speak(notify_error)
                    executor.submit(notify_task_step, spider_url, "COMPILE", task_id, errorStackTrace)
                else:
                    executor.submit(notify_task_step, spider_url, "COMPILE", task_id, "")
                    system_agent.speak("编译部署成功-请测试介入")
            else:
                executor.submit(notify_task_step, spider_url, "COMPILE", task_id, "")
                system_agent.speak("编译部署成功-请测试介入")
    except Exception as e:
        print("异常信息为", e)
        compile_status = "fail"
        pass

    return {
        "compile_status": compile_status,
        "code_error_info": code_error_info
    }


def compile_error_code(state: CodeContext):
    java_experts = state.get("java_expert")
    code_error_info = state["code_error_info"]
    # arrangement
    x = java_experts(Msg(content=code_error_info, name="Moderator", role="assistant"))

    senior_java_programming_expert = state["senior_java_programming_expert"]
    notify_msg_to_memory_msg(agents=[senior_java_programming_expert], msg=x)
    compile_error_count = state["compile_error_count"]
    if compile_error_count > 5:
        # 抛异常
        executor = state['executor']
        spider_url = state['spider_url']
        task_id = state['task_id']
        executor.submit(notify_task_step, spider_url, "COMPILE_ERROR", task_id,
                        "编译错误次数过多，请检查需求,与领域关系是否描述清楚")
        raise ValueError("编译错误次数过多，请检查代码")
    return {
        "compile_error_count": compile_error_count + 1
    }


# senior_java_programming_expert_node create_test_case_scene
def check_compile_code_router(state: CodeContext) -> Literal[
    "compile_error_code", "create_test_case_scene"]:
    compile_status = state["compile_status"]
    if compile_status == 'suss':
        return 'create_test_case_scene'
    return 'compile_error_code'


# code_organization_node compile_code
def check_organized_code_before_router(state: CodeContext) -> Literal[
    "code_organization_node", "compile_code"]:
    code_standard_check = state.get("code_standard_check")
    if code_standard_check:
        return "compile_code"
    return "code_organization_node"


def create_test_case(state: CodeContext):
    test_scenes = state['test_scenes']

    for scene in test_scenes:
        if not isinstance(scene, TestScene):
            print(f"Warning: {scene} is not an instance of TestScene")
        else:
            scene_msg = scene.get_scenes()
            print("----执行当前scene:", scene_msg)
            # test.speak("请构建用例的数据信息," + scene_msg)


# 生成测试用例
def create_test_case_scene(state: CodeContext):
    test_case_scene_agent = state['test_case_scene_agent']
    x = test_case_scene_agent()
    context_json = json.dumps(x.content, ensure_ascii=False)
    print("create_test_case_scene 源码为 {}", context_json)
    scene_result = json.loads(context_json)
    case_scene = scene_result["case_scenes"]
    # 构造测试场景
    test_scene_list = [TestScene]
    for scene in case_scene:
        print("用例场景", scene)
        test_scenes = TestScene(scene=scene, is_run=False)
        test_scene_list.append(test_scenes)
    return {
        "test_scenes": test_scene_list
    }


# 初始化测试用例需要的数据
def create_test_data(state: CodeContext):
    test_case_agent = state["test_init_data_agent"]
    x = test_case_agent()
    context_json = json.dumps(x.content, ensure_ascii=False)
    scene_result = json.loads(context_json)
    print("case_data 源码为 {}", scene_result)
    # 保存ai生成的测试数据
    method_input_param = scene_result.get("method_input_param")
    case_sql = scene_result.get("case_sql")
    task_id = state['task_id']
    domain_function_version_id = state['domain_function_version_id']
    executor = state['executor']
    spider_url = state['spider_url']
    executor.submit(notify_task_step, spider_url, "TEST", task_id, "")
    param = {
        "methodInputModes": method_input_param,
        "caseSql": case_sql,
        "taskId": task_id,
        "domainFunctionVersionId": domain_function_version_id
    }
    run_case(param)


# def dbManager(state: CodeContext):
# 聊天的chat
def chat_router(state: CodeContext) -> str:
    # 通知群内成员-
    current_role = state["current_role"]
    end = state["end"]
    print("助手为", current_role)
    if end:
        return "__end__"
    else:
        return current_role


def code_router(state: CodeContext) -> Literal[
    "senior_java_programming_expert_node", "__end__", "code_organization_node"]:
    if state["code_review_count"] < 10 and not state["meet_the_standards"]:
        # 重试超过3次 跳出校验
        return "senior_java_programming_expert_node"
    elif state["meet_the_standards"]:
        # 当校验为
        return "code_organization_node"
    return "__end__"


def check_code_router(state: CodeContext) -> Literal["code_review_node", "__end__", "code_optimization_execute"]:
    if state['is_it_optimized']:
        return "code_optimization_execute"

    support_encod = state["support_encod"]
    if support_encod:
        return "code_review_node"
    else:
        return "__end__"


def check_role_or_start_flow(x):
    return query_current_role(x.get("content"))


def load_domain_info(state: CodeContext):
    domain = state.get("domain")
    sub_domain = state.get("sub_domain")
    domain_info = query_domain_info_v1(area=domain, son_area=sub_domain)
    domain_assistant_agent = state.get("domain_assistant_agent")

    domain_function_package_prefixs = generate_package_domain_prefix(domain_info["groupId"],
                                                                     domain_info["tableName"])

    domain_user_info = {
        "domain_object_entity": "领域实体对象名称为" + domain_info[
            'domainObjectEntityName'] + "领域对象的字段详情" + domain_info[
                                    'domainObject'] + "使用过程中需要导入的包为" + domain_info[
                                    'domainObjectPackage'],

        "domain_object_service": "领域service名称为" + domain_info[
            'domainObjectServiceName'] + "使用过程中需要导入的service包" + domain_info[
                                     'domainObjectServicePackage'],
        "domain_function_package_prefix": "新增的业务类，方法入参,出参需要基于包名前缀," + domain_function_package_prefixs,
        "domain_pom_group_id": domain_info["groupId"],
        "domain_table_name": domain_info["tableName"],
        "domain_pom_version": domain_info["version"],
        "domain_all_info": domain_info
    }
    print("获取到的领域信息为:", domain_user_info)
    hub = state.get("hub_manager")
    hub.broadcast(
        Msg(content=domain_user_info, name="Moderator", role="assistant")
    )
    # 解析领域信息
    domain_assistant_agent()
    return {
        "domain_info": domain_info
    }


def load_data_flow(state: CodeContext):
    need_data_flow = state.get("need_data_flow")
    if need_data_flow:
        flow_data_agents = state.get("flow_data_agent")
        flow_data_info = state.get("flow_data_info")
        flow_data_desc = state.get("flow_data_desc")
        data_flow_all = {
            "flow_data_info": flow_data_info,
            "flow_data_desc": flow_data_desc
        }
        x = flow_data_agents(Msg(content=data_flow_all, name="Moderator", role="assistant"))
        # 通知编码,通知测试,通知代码校验
        senior_java_programming_expert = state["senior_java_programming_expert"]
        java_experts = state["java_expert"]
        test_init_data_agent = state["test_init_data_agent"]
        test_case_scene_agent = state["test_case_scene_agent"]
        agents = [senior_java_programming_expert, java_experts, test_init_data_agent, test_case_scene_agent]
        notify_msg_to_memory_msg(msg=x, agents=agents)


## 支持批量加载领域
def load_domain_info_v2(state: CodeContext):
    domain_infos = state.get("domain_info")
    domain_assistant_agent = state.get("domain_assistant_agent")
    domain_complete_info = []
    domainBaseInfos = domain_infos['domainBaseInfos']
    table_name = ""
    group_id = ""
    for domain_info in domainBaseInfos:
        table_name = table_name or domain_info["tableName"]
        group_id = group_id or domain_info["groupId"]
        domain_complete_info.append(build_domain_info(domain_info))

    prepare_data = {
        "domain_info": domain_complete_info,
        "taskComponent": domain_infos['taskComponent'],
        "taskService": domain_infos['taskService'],
    }
    print("prepare_data", prepare_data)
    # 解析领域信息
    x = domain_assistant_agent(Msg(content=prepare_data, name="Moderator", role="assistant"))
    # 把解析好的领域信息给到 以下的角色
    senior_java_programming_expert = state["senior_java_programming_expert"]
    java_experts = state["java_expert"]
    test_init_data_agent = state["test_init_data_agent"]
    test_case_scene_agent = state["test_case_scene_agent"]
    code_assistant = state["code_assistant"]
    agents = [senior_java_programming_expert, java_experts, test_init_data_agent, test_case_scene_agent, code_assistant]
    notify_msg_to_memory_msg(msg=x, agents=agents)
    executor = state['executor']
    spider_url = state['spider_url']
    task_id = state['task_id']
    executor.submit(notify_task_step, spider_url, "LOAD_DOMAIN_INFO", task_id, "").result()
    return {
        "table_name": table_name,
        "group_id": group_id
    }


def build_domain_info(domain_info: dict) -> dict:
    domain_function_package_prefixs = generate_package_domain_prefix(domain_info["groupId"],
                                                                     domain_info["tableName"])
    return {
        "domain_object_entity": "领域实体对象名称为" + domain_info[
            'domainObjectEntityName'] + "领域对象的字段详情" + domain_info[
                                    'domainObject'] + "使用过程中需要导入的包为" + domain_info[
                                    'domainObjectPackage'],

        "domain_object_service": "领域service名称为" + domain_info[
            'domainObjectServiceName'] + "使用过程中需要导入的service包" + domain_info[
                                     'domainObjectServicePackage'],
        "domain_function_package_prefix": "新增的业务类，方法入参,出参需要基于包名前缀," + domain_function_package_prefixs,
        "domain_pom_group_id": domain_info["groupId"],
        "domain_table_name": domain_info["tableName"],
        "domain_pom_version": domain_info["version"],
        "domain_all_info": domain_info,
    }


def load_case_info(state: CodeContext):
    senior_java_programming_expert = state.get("senior_java_programming_expert")
    case_code = {
        'business_code_case': java_to_markdown_code_block(business_code),
        'input_param_code_case': java_to_markdown_code_block(input_param_code),
        'out_put_param_code_case': java_to_markdown_code_block(out_put_param_code),
        'use': '按照需求编写代码过程中，请参照以上business_code_case,input_param_code_case,out_put_param_code_case 代码,严格按照案例的方式 编写代码'
    }
    # 加载case 给程序员
    notify_msg_to_memory_any(msg=case_code, agents=[senior_java_programming_expert])


def load_functional_requirement(state: CodeContext):
    business_requirements = state.get("business_requirements")
    # 把business_requirements转成str
    business_requirements_str = "\n".join(business_requirements)
    # 把业务需求通知以下角色
    senior_java_programming_expert = state["senior_java_programming_expert"]
    java_experts = state["java_expert"]
    test_init_data_agent = state["test_init_data_agent"]
    test_case_scene_agent = state["test_case_scene_agent"]
    code_assistant = state["code_assistant"]
    agents = [senior_java_programming_expert, java_experts, test_init_data_agent, test_case_scene_agent, code_assistant]
    notify_msg_to_memory_any(msg=business_requirements_str, agents=agents)


def notify_coder_task(state: CodeContext):
    task_id = state.get("task_id")
    print("任务id为:", task_id)
    # 调用spider通知任务已经完


def automatic_code_flow():
    workflow = StateGraph(CodeContext)
    # 加载领域
    workflow.add_node("load_domain", load_domain_info_v2)
    workflow.add_node("load_data_flow", load_data_flow)
    # 进行加载需求 load_case_info
    workflow.add_node("load_functional_requirement", load_functional_requirement)

    workflow.add_node("create_business_class_info", create_business_class_info)
    # 进行编码
    workflow.add_node("senior_java_programming_expert_node", senior_java_programming_expert_node)

    workflow.add_node("load_case_info", load_case_info)
    # 代码优化 code_optimization_execute
    # workflow.add_node("code_optimization_execute", code_optimization_execute)
    # 代码校验
    workflow.add_node("code_review_node", code_review_node)
    # 代码整理
    workflow.add_node("code_organization_node", code_organization_node)
    # 校验整理的代码
    # workflow.add_node("check_organized_code", check_organized_code)
    # 编译代码
    workflow.add_node("compile_code", compile_code)

    workflow.add_node("compile_error_code", compile_error_code)
    # 创建用例
    workflow.add_node("create_test_case_scene", create_test_case_scene)
    # 初始化用例需要的数据
    workflow.add_node("create_test_data", create_test_data)

    workflow.add_edge(START, "load_domain")
    workflow.add_edge("load_domain", "load_data_flow")
    workflow.add_edge("load_data_flow", "load_functional_requirement")
    workflow.add_edge("load_functional_requirement", "load_case_info")
    #
    workflow.add_edge("load_case_info", "create_business_class_info")

    workflow.add_edge("create_business_class_info", "senior_java_programming_expert_node")

    workflow.add_edge("senior_java_programming_expert_node", "code_review_node")

    workflow.add_conditional_edges(
        "code_review_node",
        # Next, we pass in the function that will determine which node is called next.
        code_router,
        {"senior_java_programming_expert_node": "senior_java_programming_expert_node",
         "code_organization_node": "code_organization_node", "__end__": END}
    )

    workflow.add_conditional_edges(
        "code_organization_node",
        # Next, we pass in the function that will determine which node is called next.
        check_code_organization,
        {"code_organization_node": "code_organization_node",
         "compile_code": "compile_code", "__end__": END}
    )

    # 编译代码
    # workflow.add_edge("code_organization_node", "compile_code")

    workflow.add_conditional_edges(
        "compile_code",
        # Next, we pass in the function that will determine which node is called next.
        check_compile_code_router,
        {"compile_error_code": "compile_error_code",
         "create_test_case_scene": "create_test_case_scene"}
    )
    workflow.add_edge("compile_error_code", "senior_java_programming_expert_node")
    # 初始化创建测试任务 并且执行
    workflow.add_edge("create_test_case_scene", "create_test_data")
    # 该流程结束
    workflow.add_edge("create_test_data", END)
    return workflow.compile()


class SpiderCodeTeamFactory:
    def __init__(self):
        # 思考需求的实现步骤
        self.technical_proposal = DialogAgent(**logical_technical_solution_config)

        self.init_test_data = SpiderDictDialogAgent(**init_test_data)

        self.senior_java_programming_expert = DialogAgent(**senior_java_programming_expert_config)

        # 代码优化 agent
        self.code_optimization_expert = DialogAgent(**code_optimization)

        # 代码优化 agent
        self.java_expert = DialogAgent(**java_expert)

        # 领域助手agent -只是通过这个agent进行根据大家交互
        self.domain_assistant_agent = DialogAgent(**domain_assistant_agent_config)
        # 代码助手，先生成业务类的名称
        self.code_assistant = SpiderDictDialogAgent(**code_assistant)
        self.code_assistant.set_parser(OutParser.class_code_name)
        # 代码规范审查 agent
        self.code_review_agent = SpiderDictDialogAgent(**code_review_agent_config)

        self.code_review_agent.set_parser(OutParser.code_review_parser)
        # 代码整理agent
        self.code_organization_agent = SpiderDictDialogAgent(**code_organization_agent_config)

        self.code_organization_agent.set_parser(OutParser.code_organization_parser)

        # 生成测试场景
        self.create_test_case_scene_agent = SpiderDictDialogAgent(**test_case_scene_engineer)
        self.create_test_case_scene_agent.set_parser(OutParser.test_case_scene)

        # 测试用例的数据准备进行测试
        self.test_case_data_init_agent = SpiderDictDialogAgent(**test_engineer)
        self.test_case_data_init_agent.set_parser(OutParser.test_case_param_and_sql)

        # 用户 agent
        self.user_agent = UserAgent(**user_agent_config)

        self.system_agent = SpiderUserAgent(**system_agent_config)
        self.system_agent.speak(system_prompt)

        self.flow_data_agent = DialogAgent(**flow_data_agent)

        self.executor = ThreadPoolExecutor(max_workers=2)
        # 自动编码
        self.automatic_code = automatic_code_flow()

    def build_automation_code_team_v2(self, param: dict):
        domain_info = param['sonDomainInfo']
        business_requirements = param["businessRequirements"]
        task_id = param['taskId']
        domain_base_id = param['baseInfoIds']
        domain_function_version_id = param['domainFunctionVersionId']
        need_Data_Flow = param['needDataFlow']
        data_flow = param['dataFlow']
        if 'flowDataDesc' in param:
            flow_data_desc = param['flowDataDesc']
        else:
            flow_data_desc = None
        self.start_automatic_flow_v2(business_requirements=business_requirements, current_role="",
                                     domain_info=domain_info, task_id=task_id, domain_base_id=domain_base_id,
                                     domain_function_version_id=domain_function_version_id,
                                     need_Data_Flow=need_Data_Flow, data_flow=data_flow, flow_data_desc=flow_data_desc)

    def start_automatic_flow_v2(self, business_requirements: str,
                                current_role: str, domain_info: dict, task_id: str, domain_base_id: list[int],
                                domain_function_version_id: str, need_Data_Flow: bool, data_flow: dict,
                                flow_data_desc: str) -> None:
        with open("spider_config.json", "r", encoding="utf-8") as f:
            model_configs = json.load(f)
            spider_url = model_configs['spider_url']
        inputs = {"business_requirements": business_requirements,
                  "senior_java_programming_expert": self.senior_java_programming_expert,
                  "code_review": self.code_review_agent,
                  "code_organization": self.code_organization_agent,
                  "domain_assistant_agent": self.domain_assistant_agent, "code_review_count": 0,
                  "system_agent": self.system_agent,
                  "support_encod": True,
                  "current_role": current_role,
                  "technical_proposal": self.technical_proposal,
                  "test_init_data_agent": self.test_case_data_init_agent,
                  "is_it_optimized": True,
                  "test_case_scene_agent": self.create_test_case_scene_agent, "domain_info": domain_info,
                  "task_id": task_id, "domain_base_id": domain_base_id,
                  "domain_function_version_id": domain_function_version_id, "code_assistant": self.code_assistant,
                  "compile_error_count": 0,
                  "java_expert": self.java_expert, "executor": self.executor, "spider_url": spider_url,
                  "flow_data_agent": self.flow_data_agent, "need_data_flow": need_Data_Flow,
                  "flow_data_info": data_flow, "flow_data_desc": flow_data_desc, "code_organization_count": 0}
        config = {"recursion_limit": 50}
        results = []
        for event in self.automatic_code.stream(inputs, config=config):
            for k, v in event.items():
                if k != "__end__":
                    results.append(v)

        # 后续处理 results 列表
        for result in results:
            # 处理每个结果
            print(result)  # 或者其他操作


def notify_msg_to_memory_any(agents: list[AgentBase], msg: Any):
    for agent in agents:
        agent.observe(Msg(content=msg, name="Moderator", role="assistant"))


def notify_msg_to_memory_msg(agents: list[AgentBase], msg: Msg):
    for agent in agents:
        agent.observe(msg)
