from fastapi import APIRouter, Depends
from typing import Annotated

from app.face_verification import FaceVerification

router = APIRouter(
    prefix="/face_verification_service",
)

@router.get('/verify')
def verify(result: Annotated[int, str, Depends(FaceVerification().verify)]):
    return result
