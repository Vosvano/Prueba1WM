from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Space
from app.schemas import SpaceCreate, SpaceResponse

router = APIRouter(prefix="/api/espacios", tags=["Espacios"])

# HTTP GET: Obtener todos los espacios
@router.get("/", response_model=list[SpaceResponse], status_code=status.HTTP_200_OK)
def listar_espacios(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(Space).all()

# HTTP POST: Crear un nuevo espacio
@router.post("/", response_model=SpaceResponse, status_code=status.HTTP_201_CREATED)
def crear_espacio(espacio: SpaceCreate, db: Session = Depends(get_db)):  # noqa: B008
    nuevo_espacio = Space(**espacio.model_dump())
    db.add(nuevo_espacio)
    db.commit()
    db.refresh(nuevo_espacio)
    return nuevo_espacio

# HTTP GET: Obtener un espacio por ID
@router.get("/{espacio_id}", response_model=SpaceResponse)
def obtener_espacio(espacio_id: int, db: Session = Depends(get_db)):  # noqa: B008
    espacio = db.query(Space).filter(Space.id == espacio_id).first()
    if not espacio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El espacio no existe"
        )
    
    return SpaceResponse.model_validate(espacio)  # Convertir a Pydantic model