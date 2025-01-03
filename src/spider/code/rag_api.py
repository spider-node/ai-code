import json

from fastapi import FastAPI, BackgroundTasks

from src.spider.code.domain.doc.spider_documents import json_convert_doc
from src.spider.code.domain.knowledge.spider_rag import SpiderRag

from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels

app = FastAPI()

background_tasks = BackgroundTasks()

with open('spider_config.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

dashScope_llm = DashScope(model_name=DashScopeGenerationModels.QWEN_MAX,
                          api_key="sk-66188116bb914e6784374de3bb394908")

rag = SpiderRag(dashScope_llm=dashScope_llm, es_url=data['es']['url'], es_user=data['es']['username'],
                es_password=data['es']['password'])


@app.post("/query_area_info")
async def say_hello(param: dict):
    response = rag.query_engine.query(param['content'])

    return {"code": 200, "data": response.response}


@app.post("/insert/doc")
async def insert_doc(doc: dict):
    """
    json转换成 doc,然后调用rag进行新增
    :param doc:
    :return:
    """
    try:
        print("insert_doc", doc)
        documents = json_convert_doc(doc)
        print("插入数据为", documents)
        rag.insert_document(documents)
    except Exception as e:
        print("insert_doc", e)
        return {"status": 500}
        pass
    return {"status": 200, "message": "ok"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8083)
