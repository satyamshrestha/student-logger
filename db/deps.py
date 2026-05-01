from db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db # Pauses the function and returns db, resumes when the request is done.
    finally:
        db.close()