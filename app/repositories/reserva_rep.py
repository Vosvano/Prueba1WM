from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.reservas import Reserva
from app.schemas.reserva_schema import ActualizarReserva, CrearReserva


# Repositorio para manejar operaciones relacionadas con las reservas en la base de datos.
class RepositorioReserva:
    def __init__(self, db: Session):
        self.db = db

    def obtener_reservas(
        self,
        salto: int = 0,
        limite: int = 10,
        usuario_id: int | None = None,
        espacio_id: int | None = None,
        fecha: date | None = None,
        estado: str | None = None
    ) -> list[Reserva]:
        query = self.db.query(Reserva)

        # 1. Filtro por Usuario
        if usuario_id is not None:
            query = query.filter(Reserva.id_usuario == usuario_id)

        # 2. Filtro por Espacio
        if espacio_id is not None:
            query = query.filter(Reserva.id_espacio == espacio_id)

        # 3. Filtro por Fecha
        if fecha is not None:
            # Comparamos solo la fecha (día)
            query = query.filter(func.date(Reserva.fecha) == fecha)

        # 4. Filtro por Estado (ej: 'Confirmada', 'Cancelada')
        if estado is not None:
            query = query.filter(Reserva.estado.ilike(f"%{estado}%"))

        return query.offset(salto).limit(limite).all()

    def obtener_reserva_id(self, id_reserva: int) -> Reserva | None:
        return self.db.query(Reserva).filter(Reserva.id == id_reserva).first()

    def obtener_reservas_activas_espacio(self, id_espacio: int, fecha: date) -> list[Reserva]:
        # Busca reservas confirmadas en ese espacio y ese día para validar solapamiento
        return self.db.query(Reserva).filter(
            Reserva.id_espacio == id_espacio,
            func.date(Reserva.fecha) == fecha,
            Reserva.estado != "Cancelada"
        ).all()

    def crear_reserva(self, datos: CrearReserva) -> Reserva:
        nueva_reserva = Reserva(**datos.model_dump())
        self.db.add(nueva_reserva)
        self.db.commit()
        self.db.refresh(nueva_reserva)
        return nueva_reserva

    def actualizar_reserva(self, reserva: Reserva, datos: ActualizarReserva) -> Reserva:
        datos_actualizar = datos.model_dump(exclude_unset=True)
        for key, value in datos_actualizar.items():
            setattr(reserva, key, value)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def eliminar_reserva(self, reserva: Reserva) -> None:
        self.db.delete(reserva)
        self.db.commit()