import os
from dotenv import load_dotenv

load_dotenv()

# 大模型API配置，替换成你的服务商（通义千问/DeepSeek/OpenAI）
LLM_API_KEY = os.getenv("LLM_API_KEY", "YOUR_API_KEY_PLACEHOLDER")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
LLM_MODEL_NAME = "qwen-turbo"

# 向量模型
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DB_PATH = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3