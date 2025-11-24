from fastapi import APIRouter

router = APIRouter(
    prefix='/ping',
    tags=['ping']
)

@router.get(path='/')
def ping():
    return {"response": "pong"}