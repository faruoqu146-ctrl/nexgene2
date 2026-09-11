from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.security import hash_password
from app.db.database import get_db
from app.db.models import Profile, User

router = APIRouter(prefix="/api/v1/dev", tags=["development"])

@router.post("/users")
def create_dev_user(email: str, password: str = "testpassword123", db: Session = Depends(get_db)):
    email = email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=email, password_hash=hash_password(password))
    db.add(user)
    db.flush()
    db.add(Profile(user_id=user.id))
    db.commit()
    return {"id": user.id, "email": user.email, "password": password}
