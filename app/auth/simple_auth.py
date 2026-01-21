from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

USERS = {
    "writer": {"password": "writer123", "role": "writer"},
    "manager": {"password": "manager123", "role": "manager"},
}

def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
):
    user = USERS.get(credentials.username)
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return {
        "username": credentials.username,
        "role": user["role"],
    }
