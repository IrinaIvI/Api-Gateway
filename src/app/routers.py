from fastapi import APIRouter, Depends
from typing import Annotated

from app.common import api_registration

router = APIRouter(
    prefix="/api_gateway",
)

@router.post('/api_registration')
def api_registration(user: Annotated[str, str, Depends(api_registration)]):
    return user
