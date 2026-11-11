
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from postgrest.exceptions import APIError

from app.auth import get_authenticated_supabase

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/me")
def get_my_profile(
    client: Annotated[
        Client,
        Depends(get_authenticated_supabase)
    ]
):
    try:
        response = (
            client.table("Student")
            .select(
                "StudentID,AuthUserID,FullName,"
                "Email,Programme,YearOfStudy,"
                "IsActive,CreatedDate,ModifiedDate"
            )
            .limit(1)
            .execute()
        )

    except APIError:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve student profile"
        ) from None

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    return response.data[0]
