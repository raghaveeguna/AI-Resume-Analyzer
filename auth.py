
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional

from ..models.resume_model import User
from ..core.database import get_database
from ..utils.security import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter()

# OAuth2PasswordBearer will be used for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=User)
async def register_user(user: User):
    db = get_database()
    users_collection = db["users"]

    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.hashed_password) # user.hashed_password will contain the plain password from input
    user.hashed_password = hashed_password
    user.created_at = datetime.utcnow()

    result = users_collection.insert_one(user.model_dump(by_alias=True))
    user.id = str(result.inserted_id)
    user.hashed_password = "********" # Mask password for response
    return user

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()
    users_collection = db["users"]

    user_doc = users_collection.find_one({"email": form_data.username})
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    user = User(**user_doc)

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=30) # Token expiration time
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except:
        raise credentials_exception
    
    db = get_database()
    users_collection = db["users"]
    user_doc = users_collection.find_one({"email": email})
    if user_doc is None:
        raise credentials_exception
    return User(**user_doc)
