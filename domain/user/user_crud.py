from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate, UserCreatePW
from models import User
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(userid=user_create.userid,
                #    password=pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   phone=user_create.phone,
                   username=user_create.username,
                   usertype=user_create.usertype,
                   nickname=user_create.nickname,
                   modify_date=datetime.now(),
                   create_date=datetime.now(),
                   sns_type=user_create.sns_type,
                   sns_id=user_create.sns_id,
                   sns_connect_date=user_create.sns_connect_date,
                   sns_name=user_create.sns_name,
                   sns_gender=user_create.sns_gender,
                   sns_age=user_create.sns_age,
                   sns_birthyear=user_create.sns_birthyear,
                   sns_birthday=user_create.sns_birthday,
                   permission= user_create.permission
                    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return { 
        'id': db_user.id,
        'userid': db_user.userid,
        'status': 'success'
    }


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.userid == user_create.userid) |
        (User.sns_id == user_create.sns_id) |
        (User.email == user_create.email)
    ).first()

def get_user(db: Session, userid: str):
    return db.query(User).filter(User.userid == userid).first()


def create_user_pw(db: Session, user_create: UserCreatePW):
    db_user = User(userid=user_create.userid,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   phone=user_create.phone,
                   username=user_create.username,
                   usertype=user_create.usertype,
                   nickname=user_create.nickname,
                   modify_date=datetime.now(),
                   create_date=datetime.now(),
                   sns_type=user_create.sns_type,
                   sns_id=user_create.sns_id,
                   sns_connect_date=user_create.sns_connect_date,
                   sns_name=user_create.sns_name,
                   sns_gender=user_create.sns_gender,
                   sns_age=user_create.sns_age,
                   sns_birthyear=user_create.sns_birthyear,
                   sns_birthday=user_create.sns_birthday,
                   permission= user_create.permission
                    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return { 
        'id': db_user.id,
        'userid': db_user.userid,
        'status': 'success'
    }