from fastapi import APIRouter, Depends
from typing import Annotated
from decimal import Decimal
from datetime import datetime

from app.common import api_registration, api_authorisation, api_create_transaction, api_get_transaction

router = APIRouter(
    prefix="/api_gateway",
)

@router.get('/api_registration')
def registration(user: Annotated[str, str, Depends(api_registration)]):
    return user

@router.post('/api_authorisation')
def authorisation(user: Annotated[str, str, Depends(api_authorisation)]):
    return user

@router.post('/api_create_transaction')
def create_transaction(user: Annotated[int, Decimal, str, Depends(api_create_transaction)]):
    return user

@router.get('/api_get_transaction')
def get_transaction(user: Annotated[int, datetime, datetime, Depends(api_get_transaction)]):
    return user
