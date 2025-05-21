from fastapi import APIRouter, Depends
from models.user_model import User
from dependencies.auth_dependencies import is_authenticated
from dto.dispatch_dto import DispatchSchema, RecipientSchema
from services.dispatch_service import RecipientService


router = APIRouter(prefix="/dispatches", tags=["dispatches"])

manager = RecipientService()

@router.get("/", status_code=200)
async def all():
    return await manager.list()

@router.get("/{id}", status_code=200)
async def get_or_none(id: str):
    return await manager.get(id=id)

@router.post("/", status_code=201)
async def create(dto: DispatchSchema, current_user: User = Depends(is_authenticated)):
    return await manager.create(user_id=current_user.id, dto=dto)

@router.patch("/", status_code=201)
async def update(id: str, dto: DispatchSchema, current_user: User = Depends(is_authenticated)):
    return await manager.update(id=id, dto=dto)
