
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from supabase_auth.errors import AuthApiError

from app.auth import get_verified_token
from app.database import get_supabase_client
from app.schemas.auth import LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(data: LoginRequest):
    client = get_supabase_client()

    try:
        response = client.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })
    except AuthApiError:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        ) from None

    if response.session is None:
        raise HTTPException(
            status_code=401,
            detail="Login session unavailable"
        )

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "token_type": "bearer",
        "user_id": response.user.id
    }


@router.get("/me")
def get_current_user(
    token: Annotated[str, Depends(get_verified_token)]
):
    client = get_supabase_client()
    response = client.auth.get_user(token)

    return {
        "user_id": response.user.id,
        "email": response.user.email
    }
