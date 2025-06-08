from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from ..database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    name = Column(VARCHAR(50), nullable=True)
    email = Column(VARCHAR(50), nullable=True)
    phone = Column(VARCHAR(20), nullable=True)
    content = Column(VARCHAR(1000), nullable=True)
    create_date = Column(DateTime, nullable=False)