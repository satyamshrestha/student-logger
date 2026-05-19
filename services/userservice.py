from models.user import User
from utils.exceptions import AppException 

class UserService():
    def get_all_users(self, db):
        return db.query(User).all()

    def update_role(self, db, username, data):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise AppException("User not found!", 404)
        user.role = data.role

        db.commit()
        return {"message": f"User updated to {data.role}!"}