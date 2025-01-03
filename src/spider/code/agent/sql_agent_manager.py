from configparser import ConfigParser

from langchain import hub
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


class SqlAgentManager:
    # 字典dict 如何指定value类型
    agent_executor_map: dict
    llm: ChatOpenAI

    def __init__(self):
        self.agent_executor_map = {}
        config = ConfigParser()
        config.read('settings.ini')
        self.url = config.get('TONG_YI', 'url')
        self.key = config.get('TONG_YI', 'key')
        self.mode = config.get('TONG_YI', 'model')
        self.llm = ChatOpenAI(
            openai_api_base=self.url,
            openai_api_key=self.key,
            model=self.mode, max_tokens=8192)

    def query_sql_agent(self, db_host: str, db_name: str):
        agent_key = db_host + ":" + db_name
        if agent_key not in self.agent_executor_map:
            return None
        # 把self.agent_executor_map[agent_key] 转成 AgentExecutor类型进行返回
        return self.agent_executor_map[agent_key]

    def add_datasource(self, datasource: dict):
        db_user: str = datasource['db_user']
        db_password: str = datasource['db_password']
        db_host: str = datasource['db_host']
        db_name: str = datasource['db_name']
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
        toolkit = SQLDatabaseToolkit(db=db, llm=self.llm)
        prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
        system_message = prompt_template.format(dialect="MySQL", top_k=5)
        agent_executor = create_react_agent(
            self.llm, toolkit.get_tools(), state_modifier=system_message
        )

        agent_key = db_host + ":" + db_name
        self.agent_executor_map[agent_key] = agent_executor
