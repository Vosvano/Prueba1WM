from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Espacio(Base):
    __tablename__ = "espacios"
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        index=True
    )
    
    nombre: Mapped[str] = mapped_column(
        nullable=False,
        index=True
    )
    
    ubicacion: Mapped[str] = mapped_column(
        nullable=False
    )
    
    capacidad: Mapped[int] = mapped_column(
        nullable=False,
        default=3
    )
    
    disponibilidad: Mapped[bool] = mapped_column(
        default=True
    )
    
    descripcion: Mapped[str | None] = mapped_column(
        nullable=True,
        default=None
    )

    reservas = relationship("Reserva", back_populates="espacio")
