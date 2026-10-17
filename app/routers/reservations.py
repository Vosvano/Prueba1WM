from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Reservation
from app.schemas import ReservationResponse

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])

#HTTP GET: Obtener todas las reservas
@router.get("/", response_model=list[ReservationResponse], status_code=status.HTTP_200_OK)
def list_reservations(db: Annotated[Session, Depends(get_db)]):
    return db.query(Reservation).all()

#HTTP GET: Obtener una reserva por ID
@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, db: Annotated[Session, Depends(get_db)]):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The reservation does not exist"
        )
    return ReservationResponse.model_validate(reservation)

#HTTP POST: Crear una nueva reserva
@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: ReservationResponse, db: Annotated[Session, Depends(get_db)]):
    new_reservation = Reservation(**reservation.model_dump())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

#HTTP PUT: Actualizar una reserva existente
@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(reservation_id: int, updated_reservation: ReservationResponse, db: Annotated[Session, Depends(get_db)]):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The reservation does not exist"
        )

    data_to_update = updated_reservation.model_dump(exclude_unset=True)
    
    for key, value in data_to_update.items():
        setattr(reservation, key, value)

    db.commit()
    db.refresh(reservation)
    return reservation

#HTTP DELETE: Eliminar una reserva
@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, db: Annotated[Session, Depends(get_db)]):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The reservation does not exist"
        )
    db.delete(reservation)
    db.commit()