# hw08
用户层（Web前端）
    ↓↑
交互模块：语音录制上传、文件上传、对话展示
    ↓↑
后端服务（Python FastAPI）
├─语音处理子模块：Whisper ASR语音转文字 / Edge-TTS文字转语音
├─文档处理子模块：PDF解析 → 文本分块 → Embedding向量编码
├─向量存储子模块：Chroma本地向量数据库
├─RAG推理子模块：检索相似文档块 → 拼接Prompt → 调用大模型生成答案
    ↓↑
底层AI模型层：
OpenAI/通义千问API（大模型生成）+ all-MiniLM（文本向量化）+ Whisper（语音）
