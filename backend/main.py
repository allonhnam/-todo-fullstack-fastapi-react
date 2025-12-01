from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
import bcrypt
from datetime import datetime, timedelta
from typing import Annotated, Optional
from pydantic import BaseModel
from models import User, Todo
import os
import uuid


class UserCreate(BaseModel):
    """User creation request model."""
    username: str
    password: str

class TodoCreate(BaseModel):
    """Todo creation request model."""
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    """Todo update request model."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Get allowed origins from environment or use defaults
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
] + [origin.strip() for origin in allowed_origins if origin.strip()]

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

def get_current_user(authorization: Optional[str] = Header(None)):
    """Get current user from JWT token."""
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return username

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

# Todo endpoints
@app.get("/todos")
async def get_todos(current_user: str = Depends(get_current_user)):
    """Get all todos for the current user."""
    try:
        todos = Todo.query(current_user)
        return [
            {
                "id": todo.todo_id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "created_at": todo.created_at.isoformat() if todo.created_at else None,
                "updated_at": todo.updated_at.isoformat() if todo.updated_at else None,
            }
            for todo in todos
        ]
    except Exception as e:
        print(f"Error fetching todos: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch todos: {str(e)}")

@app.post("/todos")
async def create_todo(todo: TodoCreate, current_user: str = Depends(get_current_user)):
    """Create a new todo."""
    try:
        todo_id = str(uuid.uuid4())
        now = datetime.utcnow()
        new_todo = Todo(
            user_id=current_user,
            todo_id=todo_id,
            title=todo.title,
            description=todo.description,
            completed=False,
            created_at=now,
            updated_at=now,
        )
        new_todo.save()
        return {
            "id": new_todo.todo_id,
            "title": new_todo.title,
            "description": new_todo.description,
            "completed": new_todo.completed,
            "created_at": new_todo.created_at.isoformat() if new_todo.created_at else None,
            "updated_at": new_todo.updated_at.isoformat() if new_todo.updated_at else None,
        }
    except Exception as e:
        print(f"Error creating todo: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create todo: {str(e)}")

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: str, current_user: str = Depends(get_current_user)):
    """Get a specific todo by ID."""
    try:
        todo = Todo.get(current_user, todo_id)
        return {
            "id": todo.todo_id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat() if todo.created_at else None,
            "updated_at": todo.updated_at.isoformat() if todo.updated_at else None,
        }
    except Todo.DoesNotExist:
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        print(f"Error fetching todo: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch todo: {str(e)}")

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo_update: TodoUpdate, current_user: str = Depends(get_current_user)):
    """Update a specific todo by ID."""
    try:
        todo = Todo.get(current_user, todo_id)
        
        if todo_update.title is not None:
            todo.title = todo_update.title
        if todo_update.description is not None:
            todo.description = todo_update.description
        if todo_update.completed is not None:
            todo.completed = todo_update.completed
        
        todo.updated_at = datetime.utcnow()
        todo.save()
        
        return {
            "id": todo.todo_id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat() if todo.created_at else None,
            "updated_at": todo.updated_at.isoformat() if todo.updated_at else None,
        }
    except Todo.DoesNotExist:
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        print(f"Error updating todo: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update todo: {str(e)}")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, current_user: str = Depends(get_current_user)):
    """Delete a specific todo by ID."""
    try:
        todo = Todo.get(current_user, todo_id)
        todo.delete()
        return {"message": "Todo deleted successfully"}
    except Todo.DoesNotExist:
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        print(f"Error deleting todo: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete todo: {str(e)}")

