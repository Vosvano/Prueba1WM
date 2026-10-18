from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.espacio_rep import RepositorioEspacio
from app.repositories.reserva_rep import RepositorioReserva
from app.repositories.usuario_rep import RepositorioUsuario
from app.schemas.reserva_schema import ActualizarReserva, CrearReserva, RespuestaReserva
from app.services.reserva_service import ReservaService

# Router para el manejo de endpoints relacionados con las reservas.
router = APIRouter(prefix="/api/reservas", tags=["Reservas"])


# Dependencias
def get_reservation_service(db: Annotated[Session, Depends(get_db)]) -> ReservaService:
    repo_reserva = RepositorioReserva(db)
    repo_usuario = RepositorioUsuario(db)
    repo_espacio = RepositorioEspacio(db)
    return ReservaService(repo_reserva, repo_usuario, repo_espacio)


# HTTP GET: Obtener todas las reservas (con filtros y paginación)
@router.get("", response_model=list[RespuestaReserva], status_code=status.HTTP_200_OK)
def listar_reservas(
    pagina: int = Query(1, ge=1, description="Número de página"),
    limite: int = Query(10, ge=1, le=100, description="Cantidad por página"),
    usuario_id: int | None = Query(None, description="Filtrar por ID de usuario"),
    espacio_id: int | None = Query(None, description="Filtrar por ID de espacio"),
    fecha: date | None = Query(None, description="Filtrar por fecha (YYYY-MM-DD)"),
    estado: str | None = Query(None, description="Filtrar por estado (Confirmada, Cancelada, etc.)"),
    service: Annotated[ReservaService, Depends(get_reservation_service)] = None
):
    return service.listar_reservas(
        pagina=pagina,
        limite=limite,
        usuario_id=usuario_id,
        espacio_id=espacio_id,
        fecha=fecha,
        estado=estado
    )


# HTTP GET: Obtener una reserva por ID
@router.get("/{id_reserva}", response_model=RespuestaReserva, status_code=status.HTTP_200_OK)
def obtener_reserva(id_reserva: int, service: Annotated[ReservaService, Depends(get_reservation_service)]):
    return service.obtener_reserva_id(id_reserva)


# HTTP POST: Crear una nueva reserva (con solapamiento)
@router.post("", response_model=RespuestaReserva, status_code=status.HTTP_201_CREATED)
def crear_reserva(reserva: CrearReserva, service: Annotated[ReservaService, Depends(get_reservation_service)]):
    return service.crear_reserva(reserva)


# HTTP PATCH: Actualización parcial de una reserva existente
@router.patch("/{id_reserva}", response_model=RespuestaReserva, status_code=status.HTTP_200_OK)
def actualizar_reserva(
    id_reserva: int,
    datos: ActualizarReserva,
    service: Annotated[ReservaService, Depends(get_reservation_service)]
):
    return service.actualizar_reserva(id_reserva, datos)


# HTTP DELETE: Eliminar una reserva
@router.delete("/{id_reserva}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_reserva(id_reserva: int, service: Annotated[ReservaService, Depends(get_reservation_service)]):
    service.eliminar_reserva(id_reserva)