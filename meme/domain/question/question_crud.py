from meme.models import Question
from sqlalchemy.orm import Session
from sqlalchemy import select, func

def get_question_list_all_0(db: Session):
    _question_list = db.query(Question)\
        .order_by(Question.id.desc())\
        # .order_by(Question.create_date.desc())\
        # .all()
    total = _question_list.count()
    question_list = _question_list.all()
    
    return total, question_list


def get_question_list_all(db: Session):
    _question_list = db.scalars(select(Question)
        .order_by(Question.id.desc()) )
        # .order_by(Question.create_date.desc())\
        # .all()
    total = db.scalar(select(func.count()).select_from(Question))
    question_list = _question_list.all()
    
    return total, question_list

def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question)\
        .order_by(Question.create_date.desc())
    # print(str(_question_list.statement.compile(compile_kwargs={"literal_binds": True})))

    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

async def get_async_question_list(db: Session, skip: int = 0, limit: int = 10):
    data = await db.scalars(select(Question)
                            .offset(skip).limit(limit)
                            .order_by(Question.create_date.desc()))
    total = await db.scalar(select(func.count()).select_from(Question))
    # total = data.count()
    question_list = data.all()
    # question_list = data.all()
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)

async def get_async_question_list_all(db: Session):
    data = await db.scalars(select(Question)
                            .order_by(Question.create_date.asc()))
    total = await db.scalar(select(func.count()).select_from(Question))
    question_list = data.all()
    return total, question_list


# async def get_async_question_list(db: Session):
#     data = await db.execute(select(Question)
#                             .order_by(Question.create_date.desc())
#                             .limit(10))
#     return data.all()