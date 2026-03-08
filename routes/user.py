from fastapi import HTTPException, Depends, APIRouter
from schemas.user import UserRequest, UserResponse, AddVocabRequest, VocabItem
from models.user import User, VocabBank
from db import get_db
from sqlalchemy import select, insert

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", status_code = 201)
def create_user(username: str, database = Depends(get_db)) -> None:
    try:
        database.execute(insert(User), [{"username": username}])
        database.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user {e}")
    
@router.get("/get/{username}", status_code=200)
def get_user_id(username: str, database = Depends(get_db)) -> int:
    try:
        user_data = database.scalars(select(User).where(User.username==username)).first()
        if not user_data:
            raise HTTPException(status_code=404, detail = "User does not exist")
        return user_data.id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user id: {e}")


@router.get("/get_user_data/{id}", status_code = 200)
def get_user_data(id: int, database = Depends(get_db)) -> UserResponse:
    try:
        user = database.scalars(select(User).where(User.id==id)).first()
        if user:
            vocab_list = [VocabItem(**v.__dict__) for v in user.vocab]
            return UserResponse(username = user.username, user_id = user.id, vocab = vocab_list)
        else:
            raise HTTPException(status_code=404, detail = "User Not Found")
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error finding user {e}")
    
@router.post("/add_vocab", status_code = 201)
def add_vocab(request: AddVocabRequest, database = Depends(get_db)) -> None:
    try:
        vocab_bank = VocabBank(**request.model_dump())
        database.add(vocab_bank)
        database.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error adding vocab {e}")
