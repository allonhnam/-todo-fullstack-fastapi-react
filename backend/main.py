from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel
from models import User
import os


class UserCreate(BaseModel):
    """User creation request model."""
    username: str
    password: str

SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bcrypt configuration
BCRYPT_ROUNDS = 12

def get_user_by_username(username: str):
    try:
        user = User.get(username)
        return user
    except User.DoesNotExist:
            return None

def hash_password(password: str) -> str:
    """Hash a password using bcrypt, handling the 72-byte limit."""
    # Bcrypt has a 72-byte limit, so we need to truncate if necessary
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string for storage
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    # Bcrypt has a 72-byte limit, so we need to truncate if necessary
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Verify password
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_user(username: str, password: str):
    hashed_password = hash_password(password)
    user = User(username=username, hashed_password=hashed_password)
    user.save()
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/register")
async def register_user(user: UserCreate):
    try:
        existing = get_user_by_username(user.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered")

        new_user = create_user(username=user.username, password=user.password)
        return {"message": "User created successfully", "username": new_user.username}
    except Exception as e:
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Backend is running"}

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate user and return access token."""
    try:
        user = get_user_by_username(form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

