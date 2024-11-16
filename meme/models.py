from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from .database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from .model import works
from .model import contact
# from meme.models import User

# print('model', portfolio.Portfolio)
# Portfolio= portfolio.Portfolio
# Works= works


class User(Base):
    __tablename__ = "user"

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
    modify_date = Column(DateTime, nullable=False)
    create_date = Column(DateTime, nullable=False)
    sns_type = Column(String(50), index=True, nullable=False)
    sns_id = Column(String(50), unique=True, nullable=False)
    sns_name = Column(String(50), nullable=True)
    sns_gender = Column(String(10), nullable=True)
    sns_age = Column(String(10), nullable=True)
    sns_birthyear = Column(String(10), nullable=True)
    sns_birthday = Column(String(10), nullable=True)
    sns_connect_date = Column(String(50), nullable=True)

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    # user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    # user = relationship("User", backref="question_users")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[List[User]] = relationship()

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    # question_id = Column(Integer, ForeignKey("question.id"))
    # question = relationship("Question", backref="answers")
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped[List[Question]] = relationship()

    # user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    # user = relationship("User", backref="answer_users")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[List[User]] = relationship()


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True)
    biz_title = Column(VARCHAR(300), nullable=False)
    channel = Column(String(50), index=True, nullable=False)
    type = Column(String(50), index=True, nullable=False)
    category = Column(String(50), index=True, nullable=False)
    content = Column(MEDIUMTEXT, nullable=False)
    address= Column(VARCHAR(300), nullable=False)
    phone = Column(String(13), nullable=False)
    msg = Column(MEDIUMTEXT, nullable=False)
    keyword = Column(Text, nullable=False)
    personnel= Column(INTEGER(5), nullable=False)
    available_dayname= Column(String(100), nullable=False)
    unvailable_dayname= Column(String(100), nullable=False)
    available_time= Column(Text, nullable=False)

    run_start_date = Column(DateTime, nullable=False)
    run_end_date = Column(DateTime, nullable=False)
    apply_start_date = Column(DateTime, nullable=False)
    apply_end_date = Column(DateTime, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[List[User]] = relationship()


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    name = Column(VARCHAR(50), nullable=True)
    value = Column(MEDIUMTEXT, nullable=True)
    status = Column(MEDIUMTEXT, nullable=True)
    doc_01 = Column(MEDIUMTEXT, nullable=True)
    doc_02 = Column(MEDIUMTEXT, nullable=True)
    modify_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[List[User]] = relationship()

