from sqlalchemy.orm import Session

from app.models.espacios import Espacio
from app.schemas.espacio_schema import ActualizarEspacio, CrearEspacio


# Repositorio para manejar operaciones relacionadas con los espacios en la base de datos.
class RepositorioEspacio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_espacios(
        self,
        salto: int = 0,
        limite: int = 10,
        capacidad: int | None = None,
        disponibilidad: bool | None = None
    ) -> list[Espacio]:
        query = self.db.query(Espacio)

        if capacidad is not None:
            query = query.filter(Espacio.capacidad >= capacidad)

        if disponibilidad is not None:
            query = query.filter(Espacio.disponibilidad == disponibilidad)

        return query.offset(salto).limit(limite).all()

    def obtener_espacio_id(self, id_espacio: int) -> Espacio | None:
        return self.db.query(Espacio).filter(Espacio.id == id_espacio).first()
    
    def crear_espacio(self, space: CrearEspacio) -> Espacio:
        nuevo_espacio = Espacio(**space.model_dump())
        self.db.add(nuevo_espacio)
        self.db.commit()
        self.db.refresh(nuevo_espacio)
        return nuevo_espacio

    def actualizar_espacio(self, espacio: Espacio, espacio_data: ActualizarEspacio) -> Espacio:
        datos = espacio_data.model_dump(exclude_unset=True)
        for key, value in datos.items():
            setattr(espacio, key, value)
        self.db.commit()
        self.db.refresh(espacio)
        return espacio

    def eliminar_espacio(self, espacio: Espacio) -> None:
        self.db.delete(espacio)
        self.db.commit()