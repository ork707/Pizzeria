from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserLogin
from app.schemas.user import UserCreate
from fastapi import HTTPException
from app.security import hash_password
from app.security import verify_password
from app.auth import create_access_token
from fastapi import Header
from app.auth import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(
        user.password
      )
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.post("/login")
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
    {"sub": user.username}
    )

    return {
    "access_token": token,
    "token_type": "bearer"
    } 


@router.get("/me")
def get_me(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.replace("Bearer ", "")

    username = verify_token(token)

    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }   