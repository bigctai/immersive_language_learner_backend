from typing import Optional, List
from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str

class VocabItem(BaseModel):
    phrase: str
    translation: str
    priority: int
    difficulty: int
    pronunciation: str

class UserResponse(BaseModel):
    username: str
    user_id: int
    vocab: List[VocabItem] = []

class AddVocabRequest(BaseModel):
    user_id: int
    phrase: str
    translation: str
    pronunciation: str
    priority: int = 1
    difficulty: int = 1
