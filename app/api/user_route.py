from app.services.user_service import UserService , User , UserCreate , UserUpdate , CRUDBase
from fastapi import APIRouter , Depends
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/user" , 
    tags=["user"]
)

def get_user_service():
    repo = CRUDBase(User)
    return UserService(repo)

@router.post("" , response_model= UserResponse)
def creat_user (
    user_data : UserCreate , 
    db : Session = Depends(get_db),
    service : UserService = Depends(get_user_service)
):
    return service.create(db , user_data)

@router.patch("" , response_model= UserResponse)
def update_user(
    user_id : int ,
    user_data : UserUpdate , 
    db : Session = Depends(get_db),
    service : UserService = Depends(get_user_service)
):
    return service.update(db , user_id , user_data)