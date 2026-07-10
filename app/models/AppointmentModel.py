

from ..db_connector import Base
from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Boolean,
    Column,
    false
)
class Appt(Base):
    __tablename__ = "appointments"
    
    # define columns
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=False, nullable=False)
    phone_number = Column(String,unique=True, nullable=False)
    appt_at = Column(DateTime(timezone=True), nullable=False)    
    reminde_date = Column(DateTime)
    sent = Column(Boolean, server_default=false(), nullable=False)# `server_default = false()` to avoid put `NULL` val in column that refuse Null values
    