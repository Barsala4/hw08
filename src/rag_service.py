import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from openai import OpenAI
from config import *

# 初始化向量数据库
embedding_fn = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="course_knowledge", embedding_function=embedding_fn)

# 大模型客户端
llm_client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL
)

def add_document_to_vector_db(chunks, doc_name):
    """将文档切片存入向量库"""
    ids = [f"{doc_name}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": doc_name}] * len(chunks)
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )

def retrieve_relevant_docs(query: str, top_k=TOP_K):
    """根据问题召回最相似文档片段"""
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results["documents"][0], results["metadatas"][0]

def generate_answer(query: str):
    """RAG构造prompt调用大模型生成答案"""
    docs, meta = retrieve_relevant_docs(query)
    context = "\n\n".join(docs)
    prompt = f"""
你是课程学习助手，请严格根据下面参考资料回答用户问题，如果资料里没有相关内容，请直接告知知识库未收录。
【参考资料】
{context}

用户问题：{query}
回答需要清晰简洁，并标注答案来自哪一份文档。
"""
    resp = llm_client.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content