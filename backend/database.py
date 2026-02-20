from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = "postgresql://postgres:root@localhost:5432/Employee_Management_System"
engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)