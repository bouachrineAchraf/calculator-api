from sqlalchemy import Column, Integer, String
from database import Base

class Calculation(Base): 
    __tablename__ = "calculation"

    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String(50))
    result = Column(String(50))

