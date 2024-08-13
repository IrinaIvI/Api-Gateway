from fastapi import APIRouter, Depends
from typing import Annotated
from decimal import Decimal
from datetime import datetime
from fastapi import UploadFile

from app.common import (
    api_authorisation,
    api_create_transaction,
    api_get_transaction,
    api_registration,
    transaction_ready,
    face_verification_ready,
    auth_ready,
    api_verify
)

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
def create_transaction(result: Annotated[int, Decimal, str, Depends(api_create_transaction)]):
    return result

@router.get('/api_get_transaction')
def get_transaction(report: Annotated[int, datetime, datetime, Depends(api_get_transaction)]):
    return report

@router.get('/api_get_transaction_health')
def transaction_ready():
    return transaction_ready

@router.get('/api_get_auth_health')
def auth_ready():
    return auth_ready

@router.get('/api_get_face_verification_health')
def face_verification_ready():
    return face_verification_ready

@router.post('/api_verify')
def verify_user(result: Annotated[int, str, UploadFile, Depends(api_verify)]):
    return result
