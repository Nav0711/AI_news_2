from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
from datetime import timedelta
from data_pipeline.utils.user_db import get_user_by_email, create_user, update_user_profile
from api.auth_utils import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class OnboardingRequest(BaseModel):
    profile_type: str
    interests: List[str]

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # converting ObjectId to str if needed
    user["_id"] = str(user["_id"])
    return user

@router.post("/register")
def register(req: RegisterRequest):
    if get_user_by_email(req.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = get_password_hash(req.password)
    user = create_user(req.email, hashed_pwd)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(req: LoginRequest):
    user = get_user_by_email(req.email)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    # exclude password hash
    return {
        "email": user["email"],
        "profile_type": user.get("profile_type"),
        "interests": user.get("interests", [])
    }

@router.post("/onboarding")
def complete_onboarding(req: OnboardingRequest, user: dict = Depends(get_current_user)):
    success = update_user_profile(user["email"], req.profile_type, req.interests)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save profile")
    return {"message": "Profile updated successfully"}
