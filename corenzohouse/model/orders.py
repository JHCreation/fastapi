from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from ..database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    content = Column(LONGTEXT, nullable=True)
    modify_date = Column(DateTime, nullable=False)
    create_date = Column(DateTime, nullable=False)