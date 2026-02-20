from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Employee(Base):

    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String)
    department = Column(String)
    salary = Column(Float)
    experience = Column(Integer)
