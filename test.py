from db.database import engine, Base
from models.student import Student

Base.metadata.create_all(bind=engine)