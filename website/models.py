from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from .database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from .config import load_models, ROOT_DIR 

load_models(ROOT_DIR / "model")

class User(Base):
    __tablename__ = "_users"

    id = Column(Integer, primary_key=True)
    userid = Column(String(100), unique=True, nullable=False)
    password = Column(String(500), nullable=True)
    email = Column(String(50), nullable=False)
    phone = Column(String(13), nullable=False)
    username = Column(String(50), nullable=True)
    usertype = Column(String(20), index=True, nullable=False)
    permission = Column(String(20), index=True, nullable=False)
    nickname = Column(String(100), nullable=True)
    orgname = Column(String(50), nullable=True)
    domain = Column(String(50), nullable=True)
    modify_date = Column(DateTime, nullable=False)
    create_date = Column(DateTime, nullable=False)


class Category(Base):
    __tablename__ = "_category"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    name = Column(VARCHAR(50), nullable=True)
    value = Column(MEDIUMTEXT, nullable=True)
    status = Column(MEDIUMTEXT, nullable=True)
    modify_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("_users.id"))
    user: Mapped[List[User]] = relationship()

