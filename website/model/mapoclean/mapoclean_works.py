from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from ...database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Works(Base):
    __tablename__ = "mapoclean_works"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    title = Column(VARCHAR(50), nullable=True)
    subject = Column(VARCHAR(150), nullable=True)
    contents = Column(LONGTEXT, nullable=True)
    # thumb = Column(MEDIUMTEXT, nullable=True)
    public = Column(VARCHAR(10), nullable=True)
    images = Column(MEDIUMTEXT, nullable=True)
    modify_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, nullable=False)