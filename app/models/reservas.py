from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# Modelo de datos para representar una reserva en la base de datos.
class Reserva(Base):
    __tablename__ = "reservas"
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        index=True
    )
    
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), 
        nullable=False,
        index=True
    )
    
    id_espacio: Mapped[int] = mapped_column(
        ForeignKey("espacios.id"), 
        nullable=False,
        index=True
    )
    
    fecha: Mapped[datetime] = mapped_column(
        nullable=False
    )
    
    hora_inicio: Mapped[datetime] = mapped_column(
        nullable=False
    )
    
    hora_fin: Mapped[datetime] = mapped_column(
        nullable=False
    )
    
    estado: Mapped[str] = mapped_column( 
        nullable=False,
        default="Confirmada"
    )

    usuario = relationship("Usuario", back_populates="reservas")
    espacio = relationship("Espacio", back_populates="reservas")