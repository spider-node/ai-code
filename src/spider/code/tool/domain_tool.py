import json
from agentscope.service import ServiceResponse, ServiceExecStatus
from src.spider.code.util.httpUtil import spider_request


def query_domain_info(son_area: str, area: str) -> ServiceResponse:
    """
    Search question in query all domain info Search API and return the searching results

    Args:
        son_area (`str`):
            son domain information that needs to be loaded
        area (`str`)
            domain information that needs to be loaded
    """
    with open("spider_config.json", "r", encoding="utf-8") as f:
        model_configs = json.load(f)
        url = model_configs['spider_url'] + "/query/son_area"
    request = {"sonArea": son_area, "area": area}
    response = spider_request(url=url, param=request)
    result = response['data']
    if result is None:
        return ServiceResponse(status=ServiceExecStatus.ERROR, content="没有查询到子域信息")
    return ServiceResponse(status=ServiceExecStatus.SUCCESS, content=result)


def query_domain_info_v1(son_area: str, area: str) -> json:
    """
    Search question in query all domain info Search API and return the searching results

    Args:
        son_area (`str`):
            son domain information that needs to be loaded
        area (`str`)
            domain information that needs to be loaded
    """
    with open("spider_config.json", "r", encoding="utf-8") as f:
        model_configs = json.load(f)
        url = model_configs['spider_url'] + "/query/son_area"
    request = {"sonArea": son_area, "area": area}
    response = spider_request(url=url, param=request)
    if response['code'] == 0:
        return response['data']
    else:
        return {}


def query_domain_rag(describe: str) -> str:
    with open("rag.json", "r", encoding="utf-8") as f:
        model_configs = json.load(f)
        url = model_configs['rag_url'] + "/query_area_info"
    request = {"content": describe}
    response = spider_request(url=url, param=request)
    return response['data']
