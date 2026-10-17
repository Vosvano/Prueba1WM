from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Space
from app.schemas import SpaceCreate, SpaceResponse, SpaceUpdate

router = APIRouter(prefix="/api/spaces", tags=["Spaces"])

# HTTP GET: Obtener todos los espacios
@router.get("/", response_model=list[SpaceResponse], status_code=status.HTTP_200_OK)
def List_spaces(db: Annotated[Session, Depends(get_db)]):
    return db.query(Space).all()

# HTTP GET: Obtener un espacio por ID
@router.get("/{space_id}", response_model=SpaceResponse)
def get_spaces(space_id: int, db: Annotated[Session, Depends(get_db)]):
    space = db.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The space does not exist"
        )
    
    return SpaceResponse.model_validate(space)

# HTTP POST: Crear un nuevo espacio
@router.post("/", response_model=SpaceResponse, status_code=status.HTTP_201_CREATED)
def create_space(space: SpaceCreate, db: Annotated[Session, Depends(get_db)]):
    new_space = Space(**space.model_dump())
    db.add(new_space)
    db.commit()
    db.refresh(new_space)
    return new_space

# HTTP PUT: Actualizar un espacio existente
@router.put("/{space_id}", response_model=SpaceResponse)
def update_space(space_id: int, updated_space: SpaceUpdate, db: Annotated[Session, Depends(get_db)]):
    space = db.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The space does not exist"
        )

    dates_to_update = updated_space.model_dump(exclude_unset=True)
    
    for key, value in dates_to_update.items():
        setattr(space, key, value)

    
    db.commit()
    db.refresh(space)
    return space

# HTTP DELETE: Eliminar un espacio
@router.delete("/{space_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_space(space_id: int, db: Annotated[Session, Depends(get_db)]):
    space = db.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The space does not exist"
        )
    
    db.delete(space)
    db.commit()