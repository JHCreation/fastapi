from passlib.context import CryptContext
from sqlalchemy.orm import Session
from corenzohouse.domain.user.user_schema import UserCreate, UserCreatePW
from models import User
from datetime import datetime


def get_user(db: Session, userid: str):
    return db.query(User).filter(User.userid == userid).first()