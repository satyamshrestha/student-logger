from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Student(Base):
    __tablename__ = "students"
    student_id = Column(String, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    courses = relationship("Course", back_populates="student")
    
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age
        }