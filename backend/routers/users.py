from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from database import get_db
from sqlalchemy.exc import IntegrityError
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime, timezone

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#!!!!!!!!!!!MUST BE HIDDEN!!!!!!!!!!!!!
SECRET_KEY = "d9761f51882304760e972428d5889860"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 60


router = APIRouter(
    prefix="/users",
    tags=["User"]
)

def hash_password(password: str):
    return context.hash(password)

def verify_password(password: str, db_password: str):
    return context.verify(password, db_password)

def get_user_with_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_pass = hash_password(user.password)
    db_user = User(username=user.username, password=hashed_pass)
    db.add(db_user)
    db.commit()
    return {"msg": "User Created"}

def authenticate_user(username: str, password: str, db: Session):
    user_in_db = get_user_with_username(db,username)
    if not user_in_db:
        return False
    if not verify_password(password, user_in_db.password):
        return False
    return user_in_db

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str =Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid Token")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid Token!")


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_in_db = get_user_with_username(db, user.username)
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already exists!")
    return create_user(db=db, user=user)


@router.post("/token")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Credentials!",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expire = timedelta(ACCESS_TOKEN_DURATION)
    token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expire
    )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/verify-token/{token}")
async def verify_client_token(token: str):
    return verify_token(token=token)
