from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.espacio_rep import RepositorioEspacio
from app.schemas.espacio_schema import ActualizarEspacio, CrearEspacio, RespuestaEspacio
from app.services.espacio_service import EspacioService

# Router para el manejo de endpoints relacionados con los espacios.
router = APIRouter(prefix="/api/espacios", tags=["Espacios"])

# Dependencias
def get_space_service(db: Annotated[Session, Depends(get_db)]) -> EspacioService:
    return EspacioService(RepositorioEspacio(db))


# GET con paginación y filtros (Query Params)
@router.get("", response_model=list[RespuestaEspacio], status_code=status.HTTP_200_OK)
def listar_espacios(
    pagina: int = Query(1, ge=1, description="Número de página"),
    limite: int = Query(10, ge=1, le=100, description="Cantidad por página"),
    capacidad: int | None = Query(None, description="Filtrar por capacidad mínima"),
    disponibilidad: bool | None = Query(None, description="Filtrar por disponibilidad"),
    service: Annotated[EspacioService, Depends(get_space_service)] = None
):
    return service.listar_espacios(pagina, limite, capacidad, disponibilidad)


# GET por ID
@router.get("/{id_espacio}", response_model=RespuestaEspacio, status_code=status.HTTP_200_OK)
def obtener_espacio_id(id_espacio: int, service: Annotated[EspacioService, Depends(get_space_service)]):
    return service.obtener_espacio_id(id_espacio)


# POST para crear
@router.post("", response_model=RespuestaEspacio, status_code=status.HTTP_201_CREATED)
def crear_espacio(data: CrearEspacio, service: Annotated[EspacioService, Depends(get_space_service)]):
    return service.crear_espacio(data)


# PUT para actualizar
@router.put("/{id_espacio}", response_model=RespuestaEspacio, status_code=status.HTTP_200_OK)
def actualizar_espacio(id_espacio: int, data: ActualizarEspacio, service: Annotated[EspacioService, Depends(get_space_service)]):
    return service.actualizar_espacio(id_espacio, data)


# DELETE para eliminar
@router.delete("/{id_espacio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_espacio(id_espacio: int, service: Annotated[EspacioService, Depends(get_space_service)]):
    service.eliminar_espacio(id_espacio)