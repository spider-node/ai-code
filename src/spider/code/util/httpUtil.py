import json

import requests


def spider_request(param: dict, url: str) -> json:
    # 发起POST请求
    try:
        response = requests.post(url, json=param)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
        return response.json()
    except requests.exceptions.HTTPError as errh:
        error = {"code": 400, "msg": errh}
    except requests.exceptions.ConnectionError as errc:
        error = {"code": 400, "msg": errc}
    except requests.exceptions.Timeout as errt:
        error = {"code": 400, "msg": errt}
    except requests.exceptions.RequestException as err:
        error = {"code": 400, "msg": err}
    return json.dumps(error)
