"""Request-scoped Supabase clients; no migrations or privileged credentials."""
from fastapi import HTTPException
from supabase import Client, ClientOptions, create_client
from app.config import get_settings

def get_supabase_client(access_token: str | None = None) -> Client:
    settings = get_settings()
    key = settings.supabase_anon_key.get_secret_value()
    if not settings.supabase_url or not key:
        raise HTTPException(503, "Supabase is not configured")
    client = create_client(
        settings.supabase_url,
        key,
        options=ClientOptions(persist_session=False, auto_refresh_token=False),
    )
    if access_token:
        # PostgREST forwards the user's JWT so existing PostgreSQL RLS applies.
        client.postgrest.auth(access_token)
    return client
