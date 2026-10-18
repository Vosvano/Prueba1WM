from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.usuario_rep import RepositorioUsuario
from app.schemas.usuario_schema import ActualizarUsuario, CrearUsuario, RespuestaUsuario
from app.services.usuario_service import UsuarioService

# Router para el manejo de endpoints relacionados con los usuarios.
router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

# Dependencias
def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UsuarioService:
    return UsuarioService(RepositorioUsuario(db))

# HTTP GET: Obtener todos los usuarios (con paginación)
@router.get("", response_model=list[RespuestaUsuario], status_code=status.HTTP_200_OK)
def obtener_usuarios(
    pagina: int = Query(1, ge=1, description="Número de página"),
    limite: int = Query(10, ge=1, le=100, description="Cantidad por página"),
    service: Annotated[UsuarioService, Depends(get_user_service)] = None
):
    return service.obtener_usuarios(pagina, limite)


# HTTP GET: Obtener un usuario por ID
@router.get("/{id_usuario}", response_model=RespuestaUsuario, status_code=status.HTTP_200_OK)
def obtener_usuario_id(id_usuario: int, service: Annotated[UsuarioService, Depends(get_user_service)]):
    return service.obtener_usuario_id(id_usuario)


# HTTP POST: Crear un nuevo usuario
@router.post("", response_model=RespuestaUsuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: CrearUsuario, service: Annotated[UsuarioService, Depends(get_user_service)]):
    return service.crear_usuario(usuario)


# HTTP PUT: Actualizar un usuario existente
@router.put("/{id_usuario}", response_model=RespuestaUsuario, status_code=status.HTTP_200_OK)
def actualizar_usuario(id_usuario: int, updated_user: ActualizarUsuario, service: Annotated[UsuarioService, Depends(get_user_service)]):
    return service.actualizar_usuario(id_usuario, updated_user)


# HTTP DELETE: Eliminar un usuario existente
@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: int, service: Annotated[UsuarioService, Depends(get_user_service)]):
    service.eliminar_usuario(id_usuario)