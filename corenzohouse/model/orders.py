from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from ..database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    # order_id = Column(VARCHAR(50), index=True, nullable=True)
    # store_id = Column(VARCHAR(50), index=True, nullable=True)
    # table_id = Column(VARCHAR(50), index=True, nullable=True)
    content = Column(LONGTEXT, nullable=True)
    # status = Column(VARCHAR(10), index=True, nullable=False)
    modify_date = Column(DateTime, nullable=False)
    create_date = Column(DateTime, nullable=False)