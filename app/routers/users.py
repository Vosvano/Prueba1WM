from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Users
from app.schemas import UserResponse

router = APIRouter(prefix="/api/users", tags=["Users"])

#HTTP GET: Obtener todos los usuarios
@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def list_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(Users).all()

#HTTP GET: Obtener un usuario por ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist"
        )
    return UserResponse.model_validate(user)

#HTTP POST: Crear un nuevo usuario
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserResponse, db: Annotated[Session, Depends(get_db)]):
    new_user = Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#HTTP PUT: Actualizar un usuario existente
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserResponse, db: Annotated[Session, Depends(get_db)]):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist"
        )

    data_to_update = updated_user.model_dump(exclude_unset=True)
    
    for key, value in data_to_update.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

#HTTP DELETE: Eliminar un usuario
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist"
        )
    
    db.delete(user)
    db.commit()