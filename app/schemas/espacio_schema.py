from pydantic import BaseModel, Field

# Esquema para la creación, actualización y respuesta de un espacio.

# Para crear un espacio
class CrearEspacio(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    capacidad: int = Field(gt=0)
    ubicacion: str = Field(min_length=3, max_length=100)
    disponibilidad: bool = Field(default=True)
    descripcion: str | None = Field(default=None, description="Descripcion opcional del espacio")


# Para actualizar un espacio correctamente (PUT)
class ActualizarEspacio(BaseModel):
    nombre: str | None = None
    capacidad: int | None = None
    ubicacion: str | None = None
    disponibilidad: bool | None = None
    descripcion: str | None = None


# Respuesta de un espacio
class RespuestaEspacio(CrearEspacio):
    id: int

    class Config:
        from_attributes = True
