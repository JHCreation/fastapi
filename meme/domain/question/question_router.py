from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from meme.database import get_db, get_async_db
from meme.domain.question import question_schema, question_crud
# from database import SessionLocal
# from models import Question
import time
import asyncio
router = APIRouter(
    prefix="/api/question",
)

# @router.get("/list", response_model=list[question_schema.Question])
# def question_list(db: Session = Depends(get_db)):
#     # _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     _question_list = question_crud.get_question_list(db)
#     return _question_list

@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 20):
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'question_list': _question_list
    }


@router.get("/list-all", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db)):
    total, _question_list = question_crud.get_question_list_all(
        db)
    # print('list-all start')
    # time.sleep(3)
    # print('list-all end')

    return {
        'total': total,
        'question_list': _question_list,
    }

@router.get("/list-next", response_model=question_schema.QuestionListNext)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 100):
    skip=page*size
    total, _question_list = question_crud.get_question_list(
        db, skip=skip, limit=size)
    count= len(_question_list) 
    isNext= skip + count >= total
    next= page + 1
    if( isNext ): next= None
    # print( skip, count, isNext, next )
    # print('list-next start')
    # time.sleep(3)
    # print('list-next end')
    print('request question /category/list')

    return {
        'nextCursor': next,
        'total': total,
        'question_list': _question_list
    }

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question

# @router.get("/list")
# def question_list():
#     # db = SessionLocal()
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     db.close()
#     return _question_list

from meme.models import Question
from datetime import datetime
@router.get("/test-create", response_model=question_schema.Question)
def question_test(db: Session = Depends(get_db)):
    for i in range(300):
        q = Question(subject='테스트 데이터입니다:[%03d]' % i, content='내용무', create_date=datetime.now())
        db.add(q)
    db.commit()


@router.get("/async_list-all", response_model=question_schema.QuestionList)
async def async_question_list_all(db: Session = Depends(get_async_db)):
    total, question_list = await question_crud.get_async_question_list_all(
        db)
    print('async_list-all start')
    await asyncio.sleep(3)
    print('async_list-all end')
    
    return {
        'total': total,
        'question_list': question_list
    }


@router.get("/async_list-next", response_model=question_schema.QuestionListNext)
async def question_list(db: Session = Depends(get_async_db),
                  page: int = 0, size: int = 100):
    skip=page*size
    total, _question_list = await question_crud.get_async_question_list(
        db, skip=skip, limit=size)
    count= len(_question_list) 
    isNext= skip + count >= total
    next= page + 1
    if( isNext ): next= None
    # print( skip, count, isNext, next )
    print('async_list-next start')
    await asyncio.sleep(3)
    print('async_list-next end')
    return {
        'nextCursor': next,
        'total': total,
        'question_list': _question_list
    }