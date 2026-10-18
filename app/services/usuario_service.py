from fastapi import HTTPException, status

from app.models.usuarios import Usuario
from app.repositories.usuario_rep import RepositorioUsuario
from app.schemas.usuario_schema import ActualizarUsuario, CrearUsuario

# Servicio para manejar la lógica de negocio relacionada con los usuarios.

class UsuarioService:
    def __init__(self, repositorio_usuario: RepositorioUsuario):
        self.repositorio_usuario = repositorio_usuario

    # Método para obtener todos los usuarios, con paginación.
    def obtener_usuarios(self, pagina: int = 1, limite: int = 10) -> list[Usuario]:
        skip = (pagina - 1) * limite
        return self.repositorio_usuario.obtener_usuarios(salto=skip, limite=limite)

    # Método para obtener un usuario por ID, verificando su existencia.
    def obtener_usuario_id(self, id_usuario: int) -> Usuario:
        user = self.repositorio_usuario.obtener_usuario_id(id_usuario)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario no existe"
            )
        return user

    # Método para crear un nuevo usuario, verificando que no exista ya.
    def crear_usuario(self, datos_usuario: CrearUsuario) -> Usuario:
        usuario_existente = self.repositorio_usuario.obtener_usuario_correo(datos_usuario.correo)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este correo"
            )
        return self.repositorio_usuario.crear_usuario(datos_usuario)

    # Método para actualizar un usuario existente.
    def actualizar_usuario(self, id_usuario: int, datos_usuario: ActualizarUsuario) -> Usuario:
        user = self.obtener_usuario_id(id_usuario)
        return self.repositorio_usuario.actualizar_usuario(user, datos_usuario)

    # Método para eliminar un usuario existente.
    def eliminar_usuario(self, id_usuario: int) -> None:
        user = self.obtener_usuario_id(id_usuario)
        self.repositorio_usuario.eliminar_usuario(user)