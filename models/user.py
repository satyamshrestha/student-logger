from db.database import Base
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    role = Column(String, default="student")
    password = Column(String)