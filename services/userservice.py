from fastapi import BackgroundTasks

from models.user import User
from utils.exceptions import AppException 
from utils.audit import log_action

class UserService():
    def get_all_users(self, db):
        return db.query(User).all()

    def update_role(self, db, username, data, background_tasks: BackgroundTasks):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise AppException("User not found!", 404)
        user.role = data.role

        db.commit()
        return {"message": f"User updated to {data.role}!"}