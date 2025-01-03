import json
import re

from agentscope.service import ServiceResponse, ServiceExecStatus
from src.spider.code.tool.CodeCase import business_code, input_param_code, out_put_param_code
from src.spider.code.util.httpUtil import spider_request


def check_business_code_package(business_code_class_name: str, business_code_class_package: str,
                                function_input_parameters_package: str, domain_group_id: str,
                                domain_table_name: str) -> ServiceResponse:
    """
    Verify the package name information of the business class

    Args:
        business_code_class_name (`str`):
            business class name
        business_code_class_package (`str`)
             business class package
        function_input_parameters_package (`str`)
            business class function input parameters class package
        domain_group_id (str)
            domain group id
        domain_table_name (`str`)
            domain table
    """
    # 根据 business_code_class_name + domain_group_id + domain_table_name 进行构造 package
    # 根据生成的名称进行判断，如果不相等，提示不匹配
    # 根据 生成的参数包名与 构造的包名进行判断

    print('进来校验代码的包名了')

    business_base_path = generate_package(domain_group_id, domain_table_name, business_code_class_name)

    business_code_class_name_new = business_base_path + ".spider.service"

    function_parameters_package_new = business_base_path + ".spider.data"
    result = {}
    if business_code_class_name_new != business_code_class_package or function_parameters_package_new != function_input_parameters_package:
        result['check_package'] = 'SUSS'
    else:
        result['check_package'] = 'FAIL'
        result['improve_business_code_package'] = 'Correct package name ' + business_code_class_name_new + ''
        result[
            'improve_function_input_parameters_package'] = 'Correct package name ' + function_parameters_package_new + ''
    return ServiceResponse(ServiceExecStatus.SUCCESS, result)


def generate_package_name(business_code_class_name: str, domain_group_id: str, domain_table_name: str):
    """
    Get the package names for the business class, input parameter class, and output parameter class
    Args:
        business_code_class_name:
            business class name
        domain_group_id:
            domain group id
        domain_table_name:
            domain table
    """
    business_base_path = generate_package(domain_group_id, domain_table_name, business_code_class_name)
    business_code_class_name_new = business_base_path + ".spider.service"

    function_parameters_package_new = business_base_path + ".spider.data"
    result = {
        'business_code_class_package_name': business_code_class_name_new,
        'function_parameters_package_name': function_parameters_package_new
    }
    return ServiceResponse(ServiceExecStatus.SUCCESS, result)


def load_code_case_data(is_there_code_case: bool) -> ServiceResponse:
    """
    When the case does not exist Load code_case
    Args:
        is_there_code_case:
            If the case does not exist, return false; if it exists, return true
    """
    if not is_there_code_case:
        code_case = {
            'business_code': business_code,
            'input_param_code': input_param_code,
            'out_put_param_code': out_put_param_code
        }
        return ServiceResponse(ServiceExecStatus.SUCCESS, code_case)


def camel_to_dot(camel_str):
    # 将驼峰命名转换为点分隔命名
    parts = re.findall(r'[A-Z][^A-Z]*', camel_str)
    return '.'.join(part.lower() for part in parts)


def generate_package(group_id, table_name, business_code_class_name):
    # 获取参数，优先使用params中的值

    # 替换table_name中的下划线为点
    table_name_new = table_name.replace('_', '.')

    # 转换business_code_class_name为点分隔的命名
    business_code_class_name = camel_to_dot(business_code_class_name)

    # 拼接最终的包名
    return f"{group_id}.{table_name_new}.{business_code_class_name}"


def generate_package_domain_prefix(group_id, table_name):
    table_name_new = table_name.replace('_', '.')
    return f"{group_id}.{table_name_new}"


def deploy_code_to_application_tool(business_code: str, param_code: str, result_code: str, table_name: str,
                                    datasource: str, task_component: str, task_service: str) -> ServiceResponse:
    """
    Deploy business code
    Args:
        business_code (`str`):
            Code for business layer classes
        param_code (`str`):
            The parameter class code for business layer methods
        result_code (`str`)
            When the return parameter object of a business method is a domain object, no information is returned
        table_name (`str`)
            table name in the domain object
        datasource (`str`)
            datasource in the domain object
        task_component (`str`)
            The value of the name attribute in @ TaskComponent in the business class
        task_service (`str`)
            The name attribute of @ TaskService annotation in business methods
    """
    request = {
        'serviceClass': business_code,
        'paramClass': param_code,
        'resultClass': result_code,
        'tableName': table_name,
        'datasource': datasource,
        'taskComponent': task_component,
        'taskService': task_service
    }

    with open("spider_config.json", "r", encoding="utf-8") as f:
        model_configs = json.load(f)
        url = model_configs['spider_url'] + "/deploy/plugin"
        result = spider_request(url=url, param=request)
    return ServiceResponse(ServiceExecStatus.SUCCESS, result)


def deploy_code_to_application(business_code: str, param_code: str, result_code: str,
                               table_name: str,
                               datasource: str, task_component: str, task_service: str, domain_base_id: list[int],
                               task_id: int, domain_function_version_id: str, maven_pom: str, spider_url: str) -> json:
    """
    部署-ai生成的代码
    :param task_service:
    :param task_component:
    :param business_code:
    :param param_code:
    :param result_code:
    :param table_name:
    :param datasource:
    :return: 部署后的信息
    """
    request = {
        'serviceClass': business_code,
        'paramClass': param_code,
        'resultClass': result_code,
        'tableName': table_name,
        'datasource': datasource,
        'taskComponent': task_component,
        'taskService': task_service,
        'baseInfoId': domain_base_id,
        'taskId': task_id,
        'domainFunctionVersionId': domain_function_version_id,
        'mavenPom': maven_pom
    }
    url = spider_url + "/deploy/plugin"
    return spider_request(url=url, param=request)


def unload_code(area_plugin: str, version: str) -> json:
    """
    卸载插件
    :param area_plugin:
    :param version:
    :return:
    """
    return None


def check_package_business_code_v1(business_class_name: str, business_class_package: str,
                                   function_input_parameters_package: str, table_name: str, group_id: str,
                                   business_class: str) -> json:
    """
    Verify whether the package name introduced in the business class is correct with one's own package name
    Args:
        business_class_name (`str`):
            generated business code class name
        business_class_package (`str`):
            The package name of the latest business code
        function_input_parameters_package (`str`):
            Method input package name in business code
        table_name (`str`):
            table name in the domain object
        group_id (`str`):
            GroupId in the domain object
        service_package (`str`):
            domainObjectServicePackage in the domain object
        domainObject_package (`str`):
            domainObjectPackage in the domain object
        business_class(`str`)
            The latest generated business code class
    """
    print("业务代码", business_class)
    non_conformance_specification = []

    correct_business_package = generate_package(group_id, table_name, business_class_name) + ".spider.service"
    is_improvement = True
    if correct_business_package != business_class_package:
        is_improvement = False
        non_conformance_specification.append(
            "业务类" + business_class_name + "代码包名为" + business_class_package + "包名不正确,正确的包名为" + correct_business_package)

    if function_input_parameters_package not in business_class:
        is_improvement = False
        non_conformance_specification.append(
            "业务类中入参,出参类的包不存在，或者导入的不正确，正确的包名为" + function_input_parameters_package + "请导入正确的入参，出参类包名")
    if business_class:

        if "com.alipay.sofa.runtime.api.annotation.SofaService" not in business_class:
            non_conformance_specification.append(
                "业务代码中 @SofaService导入包错误,请正确的导入 com.alipay.sofa.runtime.api.annotation.SofaService 包")

        if "@NoticeScope" in business_class:
            if "cn.spider.framework.annotation.NoticeScope" not in business_class:
                non_conformance_specification.append(
                    "业务代码中 没有正确import 导入 cn.spider.framework.annotation.NoticeScope,请修正")
            if "cn.spider.framework.annotation.enums.ScopeTypeEnum" not in business_class:
                non_conformance_specification.append(
                    "业务代码中没有正确import 导入 cn.spider.framework.annotation.enums.ScopeTypeEnum,请修正 ")

        if "cn.spider.framework.annotation.TaskComponent" not in business_class:
            non_conformance_specification.append(
                "业务代码中没有正确import 导入 cn.spider.framework.annotation.TaskComponent,请修正 ")

        if "cn.spider.framework.annotation.TaskService" not in business_class:
            non_conformance_specification.append(
                "业务代码中没有正确import 导入 cn.spider.framework.annotation.TaskService,或者没有使用@TaskService请修正 ")
        if "@SofaService" not in business_class:
            non_conformance_specification.append(
                "业务类中没有包含@SofaService,或者没有导入com.alipay.sofa.runtime.api.annotation.SofaService,请在业务类中添加")
    return {
        "improve": non_conformance_specification,
        "is_improvement": is_improvement
    }


def query_area() -> json:
    with open("spider_config.json", "r", encoding="utf-8") as f:
        model_configs = json.load(f)
        url = model_configs['spider_url'] + "/query/area_all_info"
    request = {}
    return spider_request(url=url, param=request)


def notify_task_step(spider_url: str, step: str, task_id: str, error: str):
    request = {
        "step": step,
        "error": error,
        "spiderDomainFunctionTaskId": task_id
    }
    url = spider_url + "/sync_ai_coder_step"
    return spider_request(url=url, param=request)


def query_area_local() -> json:
    return {
        "son_area_infos": [
            {
                "id": 2,
                "areaId": "e5fcafcc-a249-4291-b353-a169ab6d04f1",
                "areaName": "库存域",
                "sonAreaName": "商品库存",
                "tableName": "stock",
                "datasource": "spider_demo",
                "createTime": "2024-08-14T15:30:38"
            }
        ]
    }
