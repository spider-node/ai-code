import json

from src.spider.code.util.httpUtil import spider_request


def run_case(param: dict) -> json:
    with open("spider_config.json", "r", encoding="utf-8") as f:
        model_configs = json.load(f)
        url = model_configs['spider_url'] + "/run_case"
    return spider_request(url=url, param=param)
