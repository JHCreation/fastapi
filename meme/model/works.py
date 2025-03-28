from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from ..database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Works(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    title = Column(VARCHAR(50), nullable=True)
    subject = Column(VARCHAR(150), nullable=True)
    content = Column(LONGTEXT, nullable=True)
    thumb = Column(MEDIUMTEXT, nullable=True)
    create_date = Column(DateTime, nullable=False)