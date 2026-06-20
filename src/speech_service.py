import whisper
import edge_tts
import tempfile
import os

# 加载轻量版whisper模型，第一次运行会自动下载
whisper_model = whisper.load_model("base")

def speech_to_text(audio_file_path: str) -> str:
    """语音转文字 ASR"""
    result = whisper_model.transcribe(audio_file_path, language="zh")
    return result["text"]

async def text_to_speech(text: str, save_path: str):
    """文字转语音，生成mp3音频"""
    voice = "zh-CN-YunyangNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save_sync(save_path)