import datetime

from pydantic import BaseModel

from meme.domain.answer.answer_schema import Answer

class Question(BaseModel):
    id: int
    subject: str | None = None
    # content: str
    create_date: datetime.datetime
    answers: list[Answer] = []

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

class QuestionListNext(QuestionList):
    nextCursor: int | None

class QuestionAll(BaseModel):
    id: int
    subject: str | None = None
    content: str
    create_date: datetime.datetime
