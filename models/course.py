from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(String, primary_key=True)
    title = Column(String)

    student_id = Column(String, ForeignKey("students.student_id"))
    student = relationship("Student", back_populates="courses")