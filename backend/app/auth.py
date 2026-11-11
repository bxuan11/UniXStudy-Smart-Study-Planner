"""Dependencies for future protected routes; no auth endpoints registered yet."""
from typing import Annotated
import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client
from supabase_auth.errors import AuthApiError
from app.database import get_supabase_client

bearer = HTTPBearer(auto_error=False)

def get_verified_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> str:
    if credentials is None:
        raise HTTPException(401, "Bearer token required", headers={"WWW-Authenticate": "Bearer"})
    client = get_supabase_client()
    try:
        # Verify with Supabase Auth; never trust a locally decoded payload alone.
        response = client.auth.get_user(credentials.credentials)
    except AuthApiError as exc:
        if exc.status in (400, 401, 403, 422):
            raise HTTPException(401, "Invalid or expired token", headers={"WWW-Authenticate": "Bearer"}) from None
        raise HTTPException(503, "Authentication service unavailable") from None
    except httpx.HTTPError:
        raise HTTPException(503, "Authentication service unavailable") from None
    if response is None or response.user is None:
        raise HTTPException(401, "Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    return credentials.credentials

def get_authenticated_supabase(
    token: Annotated[str, Depends(get_verified_token)],
) -> Client:
    return get_supabase_client(token)
