import json
import re
from src.spider.code.chat.chat_keywords import operations_assistant, spider_domain_assistant, spider_code_expert


# 截取字符串中，是否包含 @table 并且获取出[里面的值]
def extract_table_info(s):
    # 首先检查字符串是否包含 @table
    if 'domain' in s:
        # 使用正则表达式匹配 @table['...'] 的模式
        match = re.search(r"domain\['(.*?)'\]", s)
        if match:
            # 提取方括号中的内容
            table_info = match.group(1)
            return table_info
    return None


def area_info_split(message: str) -> dict:
    if 'domain' in message:
        match = re.search(r"domain\['(.*)'\]", message)
        if match:
            full_domain = match.group(1)
            domain_parts = full_domain.split('.')
            # 创建字典
            data = {
                "area": domain_parts[0],
                "sub_area": domain_parts[1]
            }
            # 转换为JSON格式的字符串
            return data
    else:
        return None


# 校验是否确认步骤,进行编码
def check_is_code(s):
    if 'confirm_plan' in s:
        return True
    else:
        return False


# 校验用户是否取消本次沟通
def check_is_cancel(s):
    if 'exit' in s:
        return True
    else:
        return False


def query_current_role(s):
    # 运维助手
    if operations_assistant in s:
        return "code_organization_node"
    # 领域助手
    elif spider_domain_assistant in s:
        return "domain_assistant_node"
    # 编程助手
    elif spider_code_expert in s:
        return "senior_java_programming_expert_node"
    else:
        return ""
