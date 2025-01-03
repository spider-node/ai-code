import json

from llama_index.core import VectorStoreIndex, StorageContext, Settings, Document
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.dashscope import DashScopeEmbedding, DashScopeTextEmbeddingModels, \
    DashScopeTextEmbeddingType
from llama_index.llms.dashscope import DashScope
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

from src.spider.code.domain.doc.spider_documents import init_area_info, init_local_doc


class SpiderRag:
    def __init__(self, dashScope_llm: DashScope, es_url: str, es_user: str, es_password: str):
        # es客户端
        vector_store = ElasticsearchStore(
            es_url=es_url,
            index_name="spider_rag_v6",
            es_user=es_user,
            es_password=es_password
        )
        Settings.llm = dashScope_llm

        Settings.embed_model = DashScopeEmbedding(
            model_name=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V2,
            text_type=DashScopeTextEmbeddingType.TEXT_TYPE_DOCUMENT,
            api_key="sk-66188116bb914e6784374de3bb394908"
        )

        Settings.node_parser = SimpleNodeParser(chunk_size=512, chunk_overlap=20)
        Settings.num_output = 512
        Settings.context_window = 3900

        # 5. 加载索引并执行查询
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        documents = init_local_doc()
        self.index = VectorStoreIndex.from_documents(
            documents=documents,
            storage_context=storage_context
        )
        # 保存索引以便后续加载
        self.index.storage_context.persist(persist_dir=".")
        self.query_engine = self.index.as_query_engine(llm=dashScope_llm)

    def update_document(self, doc_id: str, new_text: json, document_type: str):
        """
        更新向量数据库中，领域相关的向量
        :param document_type: 文档
        :param doc_id:
        :param new_text:
        :return:
        """
        # 删除旧的Document
        self.index.delete_ref_doc(doc_id)

        self.insert_document(new_text, document_type)
        # 添加新的Document

    def delete_document(self, doc_id):
        # 删除Document
        self.index.delete_ref_doc(doc_id)

    def insert_document(self, doc: [Document]):
        for document in doc:
            self.index.insert(document)

    def init_spider_doc(self):
        """
        启动spider-code后，初始化 spider领域中的一些功能信息
        :return:
        """
        docs = init_area_info()
        for document in docs:
            self.index.insert(document)
