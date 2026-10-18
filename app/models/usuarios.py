from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# Modelo de datos para representar un usuario en la base de datos.
class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        index=True
    )
    
    nombre: Mapped[str] = mapped_column(
        nullable=False,
        index=True
    )
    
    correo: Mapped[str] = mapped_column(
        nullable=False, 
        unique=True
    )

    reservas = relationship("Reserva", back_populates="usuario")