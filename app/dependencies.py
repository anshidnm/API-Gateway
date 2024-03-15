from database import SessionLocal
from fastapi import Depends
from typing_extensions import Annotated
from auth.jwt_authentication import (
    JwtBearer
)


async def get_current_user(
        user_id: Annotated[int, Depends(JwtBearer(auto_error=False))]
    ):
    return user_id


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
