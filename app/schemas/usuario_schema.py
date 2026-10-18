from pydantic import BaseModel, Field

# Esquema para la creación, actualización y respuesta de un usuario.

# Para crear un usuario
class CrearUsuario(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    correo: str = Field(min_length=5, max_length=100)


# Para actualizar un usuario
class ActualizarUsuario(BaseModel):
    nombre: str | None = Field(default=None, min_length=3, max_length=100)
    correo: str | None = Field(default=None, min_length=5, max_length=100)


# Respuesta de un usuario
class RespuestaUsuario(BaseModel):
    id: int
    nombre: str
    correo: str

    class Config:
        from_attributes = True