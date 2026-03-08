from fastapi import HTTPException, Depends, APIRouter
import requests
from dotenv import load_dotenv
import os
from google.cloud import translate_v2 as translate
from pypinyin import pinyin, Style

load_dotenv()

client=translate.Client.from_service_account_json("/Users/christai/Desktop/immersive_language_learner_backend/routes/languagelearner-489202-4b30a6ea413f.json")


router = APIRouter(prefix="/translate", tags=["user"])

@router.get("/phrase", status_code=200)
def translate_phrase(phrase: str):
    try:
        translation = client.translate(phrase, source_language="en-US", target_language="zh-TW")
        chinese_text = translation["translatedText"]

        pinyin_list = pinyin(chinese_text, style=Style.NORMAL)
        pinyin_text = " ".join([p[0] for p in pinyin_list])
        return {
            "original": phrase,
            "chinese": chinese_text,
            "pinyin": pinyin_text
        }
    except Exception as e:
        print(f"Error: {e}")
        return f"Error tranlsating: {e}"
