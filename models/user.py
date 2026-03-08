from typing import List
from typing import Optional
from db import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(index=True)

    vocab: Mapped[List["VocabBank"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class VocabBank(Base):
    __tablename__ = "vocab_bank"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    phrase: Mapped[str] = mapped_column(index=True)
    translation: Mapped[str] = mapped_column(index=True)
    priority: Mapped[int] = mapped_column(index=True)
    difficulty: Mapped[int] = mapped_column(index=True)
    pronunciation: Mapped[str] = mapped_column(index=True)

    user: Mapped["User"] = relationship(back_populates="vocab")

