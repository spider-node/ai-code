import os

from src.spider.code.domain.knowledge.spider_rag import SpiderRag

if __name__ == '__main__':
    os.environ["DASHSCOPE_API_KEY"] = "sk-66188116bb914e6784374de3bb394908"

    rag = SpiderRag()
    rag.query_engine.query("库存域中有那些属性")
