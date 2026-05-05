from fastapi import HTTPException, Depends
from auth.deps import get_current_user

ROLE_PERMISSIONS = {
    "admin": ["create", "read", "update", "delete", "admin_only"],
    "teacher": ["create", "read", "update"],
    "student": ["read"]
}

def require_permission(permission: str):
    def checker(user: dict = Depends(get_current_user)):
        role = user.get("role")
        allowed_permissions = ROLE_PERMISSIONS.get(role, [])

        if permission not in allowed_permissions:
            raise HTTPException(status_code=403, detail="You do not have permission to perform this action!")
        
        return user
    return checker