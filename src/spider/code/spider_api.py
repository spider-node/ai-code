import json
from multiprocessing import Process
from fastapi import FastAPI
import agentscope
from agentscope.prompt import SystemPromptComparer, ChineseSystemPromptGenerator, EnglishSystemPromptGenerator
from src.spider.code.agent.spider_code_team_factory import SpiderCodeTeamFactory
from src.spider.code.agent.sql_agent_manager import SqlAgentManager
from src.spider.code.config.agent_config import senior_java_programming_expert_config, code_assistant
from src.spider.code.config.model_config import model_config

app = FastAPI()

sql_agent_factory = SqlAgentManager()

with open("spider_config.json", "r", encoding="utf-8") as f:
    model_configs = json.load(f)
    studio_url = model_configs['studio_url']


@app.post("/ai_code")
async def read_root(param: dict):
    p = Process(target=start_spider, args=[param["project_name"], studio_url])
    p.start()
    return {"code": 200}


@app.post("/optimize_prompt_words")
async def optimize_prompt_words(param: dict):
    agentscope.init(
        model_configs=model_config,
        project="优化提示词",
        name="spider",
        studio_url=studio_url,
    )
    prompt_generator = ChineseSystemPromptGenerator(
        model_config_name="qwen_config_max"
    )

    generated_system_prompt = prompt_generator.generate(
        user_input=senior_java_programming_expert_config['sys_prompt']
    )

    print(generated_system_prompt)

    return {"code": 200}


# 提供给spider进行code任务编写的接口
@app.post("/ai_code_automatic")
async def read_root(param: dict):
    p = Process(target=start_spider_automatic, args=[param, param["projectName"], studio_url])
    p.start()
    return {"code": 200}


# 提供给spider进行code任务编写的内容
def start_spider_automatic(param: dict, project: str, studio_urls: str):
    """
        开启聊天进行功能开发
        :param sql_agent:
        :param param:
        :param studio_urls:
        :param project:
        :return:
        """

    agentscope.init(
        model_configs=model_config,
        project=project,
        name="spider",
        studio_url=studio_urls,
    )
    factory = SpiderCodeTeamFactory()
    factory.build_automation_code_team_v2(param)


def start_spider(project: str, studio_urls: str):
    """
    开启聊天进行功能开发
    :param studio_urls:
    :param project:
    :return:
    """

    agentscope.init(
        model_configs=model_config,
        project=project,
        name="spider",
        studio_url=studio_urls,
    )
    factory = SpiderCodeTeamFactory()
    factory.build_team()


# 新增 领域rag
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8084)
