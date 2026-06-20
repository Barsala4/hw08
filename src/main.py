import streamlit as st
import asyncio
import tempfile
import os
from file_parser import extract_pdf_text, split_text
from rag_service import add_document_to_vector_db, generate_answer
from speech_service import speech_to_text, text_to_speech
from config import CHUNK_SIZE, CHUNK_OVERLAP

st.set_page_config(page_title="课程知识库语音问答助手", layout="wide")
st.title("📚 基于RAG的AI课程语音问答系统")

# 侧边栏：PDF文档上传
with st.sidebar:
    st.header("📂 上传课程PDF文档")
    uploaded_file = st.file_uploader("选择PDF文件", type="pdf")
    if uploaded_file is not None:
        if st.button("导入知识库"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            # 解析并切片存入向量库
            full_text = extract_pdf_text(tmp_path)
            text_chunks = split_text(full_text, CHUNK_SIZE, CHUNK_OVERLAP)
            add_document_to_vector_db(text_chunks, uploaded_file.name)
            st.success(f"✅ {uploaded_file.name} 已成功加入知识库！")
            os.unlink(tmp_path)

# 主界面：问答区域
tab1, tab2 = st.tabs(["文字问答", "语音提问"])

with tab1:
    user_text = st.text_input("输入你的问题：")
    if st.button("AI回答") and user_text:
        with st.spinner("正在检索知识库并生成答案..."):
            ans = generate_answer(user_text)
            st.markdown("### 🤖 AI回答")
            st.write(ans)

with tab2:
    st.info("上传音频文件，即可用语音提问")
    audio_file = st.file_uploader("上传语音(wav/mp3)", type=["mp3", "wav"])
    if audio_file is not None and st.button("语音转文字并问答"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tmp_audio.write(audio_file.read())
            audio_path = tmp_audio.name
        with st.spinner("正在识别语音..."):
            query_text = speech_to_text(audio_path)
            st.success(f"识别出问题：{query_text}")
            # RAG生成回答
            answer = generate_answer(query_text)
            st.markdown("### 🤖 AI回答")
            st.write(answer)
            # 生成语音回复
            voice_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            asyncio.run(text_to_speech(answer, voice_tmp.name))
            st.audio(voice_tmp.name, format="audio/mp3")
        os.unlink(audio_path)

st.divider()
st.caption("AI课程期末大作业：RAG知识库+语音交互AI应用")