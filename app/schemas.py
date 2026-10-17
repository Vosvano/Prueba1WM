from datetime import datetime

from pydantic import BaseModel, Field


# Para crear un espacio
class SpaceCreate(BaseModel):
    name: str = Field(min_length=10, max_length=100),
    capacity: int = Field(gt=2),
    location: str = Field(min_length=5, max_length=100)
    full_availability: bool = Field(default=True)   

# Para actualizar un espacio correctamente
class SpaceUpdate(BaseModel):
    name: str | None = None,
    capacity: int | None = None,
    location: str | None = None,
    full_availability: bool | None = None

# Respuesta de un espacio
class SpaceResponse(SpaceCreate):
    id: int
    class Config:
        from_attributes = True

# Para solicitar una reserva
class ReservationCreate(BaseModel):
    space_id: int = Field(gt=0),
    user_id: int = Field(gt=0),
    date: datetime = Field(default_factory=datetime.now),
    start_time: datetime = Field(default_factory=datetime.now),
    end_time: datetime = Field(default_factory=datetime.now)

# Respuesta de una reserva
class ReservationResponse(ReservationCreate):
    id: int
    status: str
    class Config:
        from_attributes = True

# Para crear un usuario
class UserCreate(BaseModel):
    name: str = Field(min_length=4, max_length=100)
    email: str = Field(min_length=10, max_length=100)

# Respuesta de un usuario
class UserResponse(BaseModel):
    id: int
    class Config:
        from_attributes = True