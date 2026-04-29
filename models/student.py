from sqlalchemy import Column, Integer, String
from db.database import Base

class Student(Base):
    __tablename__ = "students"
    student_id = Column(String, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    
    def to_dict(self):
        return {
            "student_id": self.student_id, 
            "name": self.name, 
            "age": self.age
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["age"])