
from fastapi import APIRouter

router = APIRouter()

@router.get('/users', status_code=200)
async def get_recipes():
    return {"message": "Hello World"}