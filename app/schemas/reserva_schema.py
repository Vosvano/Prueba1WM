from datetime import datetime

from pydantic import BaseModel, Field

# Esquema para la creación, actualización y respuesta de reservas.

# Para solicitar una reserva
class CrearReserva(BaseModel):
    id_usuario: int = Field(gt=0, description="ID del usuario que reserva")
    id_espacio: int = Field(gt=0, description="ID del espacio a reservar")
    fecha: datetime = Field(default_factory=datetime.now, description="Fecha de la reserva")
    hora_inicio: datetime = Field(default_factory=datetime.now, description="Hora de inicio de la reserva")
    hora_fin: datetime = Field(default_factory=datetime.now, description="Hora de fin de la reserva")


# Para actualizar parcialmente una reserva (PATCH)
class ActualizarReserva(BaseModel):
    fecha: datetime | None = None
    hora_inicio: datetime | None = None
    hora_fin: datetime | None = None
    estado: str | None = None


# Respuesta de una reserva
class RespuestaReserva(BaseModel):
    id: int
    id_usuario: int
    id_espacio: int
    fecha: datetime
    hora_inicio: datetime
    hora_fin: datetime
    estado: str

    class Config:
        from_attributes = True