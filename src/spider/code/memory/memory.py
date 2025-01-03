import os

from mem0 import Memory

os.environ["OPENAI_API_KEY"] = "sk-66188116bb914e6784374de3bb394908"

os.environ["OPENAI_API_BASE"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"

config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j://47.109.67.130:7687",
            "username": "neo4j",
            "password": "aB.967426"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "qwen-plus",
            "temperature": 0.2,
            "max_tokens": 15000,
        }
    },
    "version": "v1.1"
}

m = Memory.from_config(config_dict=config)
