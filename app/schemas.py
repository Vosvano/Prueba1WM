from datetime import datetime

from pydantic import BaseModel


# Para crear un espacio
class SpaceCreate(BaseModel):
    name: str
    capacity: int
    location: str

# Respuesta de un espacio
class SpaceResponse(SpaceCreate):
    id: int
    full_availability: bool
    class Config:
        from_attributes = True

# Para solicitar una reserva
class ReservationCreate(BaseModel):
    space_id: int
    user_id: int
    date: datetime
    start_time: datetime
    end_time: datetime

# Respuesta de una reserva
class ReservationResponse(ReservationCreate):
    id: int
    status: str
    class Config:
        from_attributes = True