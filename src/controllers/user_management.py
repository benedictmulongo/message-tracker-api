from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from src.models.schema.user import UserResponse, UserRequest, UserRequestUpdatable
from src.models.data.tracker import User
from src.database.connector import get_db
from src.repository.user import UserRepository
from typing import Optional, List
from sqlalchemy.orm import Session, query

router = APIRouter(
    prefix="/user",
    tags=["User management"],
    responses={404: {"description": "Not found"}},
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    userRepository: UserRepository = UserRepository(db)
    return userRepository.get_all_users()

@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserResponse) # Query parameters
def add_user(request: UserRequest, db: Session = Depends(get_db)):
    userRepository: UserRepository = UserRepository(db)
    new_user_data = jsonable_encoder(request)
    new_user = User(**new_user_data)
    resp = userRepository.insert_user(new_user)
    print(resp)
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    userRepository: UserRepository = UserRepository(db)
    return userRepository.get_user_by_id(id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    userRepository: UserRepository = UserRepository(db)
    userRepository.delete_user(id)

@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=UserResponse)
def patch_user(id: int, request: UserRequestUpdatable, db: Session = Depends(get_db)):
    userRepository: UserRepository = UserRepository(db)
    return userRepository.update_user(id, request)


"""
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def put_user(id: int, request: schemas.User, db: Session = Depends(database.get_db)):
    #return user.put_overwrite_if_exist(id, request, db)
    # PUT ===> for checking if resource exists then update, else create new resource
    current_user = db.query(models.User).filter(models.User.id==id)
    if not current_user.first():
        return create(request, db)
    update_key = jsonable_encoder(request)
    current_user.update(update_key)
    db.commit()
    return request
"""
