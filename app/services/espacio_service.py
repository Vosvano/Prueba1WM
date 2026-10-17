from fastapi import HTTPException, status

from app.models.espacios import Espacio
from app.repositories.espacio_rep import RepositorioEspacio
from app.schemas.espacio_schema import ActualizarEspacio, CrearEspacio


class EspacioService:
    def __init__(self, repo: RepositorioEspacio):
        self.repo = repo

    def listar_espacios(
        self, pagina: int = 1, limite: int = 10, capacidad: int | None = None, disponibilidad: bool | None = None
    ) -> list[Espacio]:
        salto = (pagina - 1) * limite
        return self.repo.obtener_espacios(salto=salto, limite=limite, capacidad=capacidad, disponibilidad=disponibilidad)

    def obtener_espacio_id(self, id_espacio: int) -> Espacio:
        espacio = self.repo.obtener_espacio_id(id_espacio)
        if not espacio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="El espacio no existe"
            )
        return espacio

    def crear_espacio(self, data: CrearEspacio) -> Espacio:
        # Validación: Capacidad debe ser mayor a 0
        if data.capacidad <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La capacidad debe ser mayor a 0"
            )
        return self.repo.crear_espacio(data)

    def actualizar_espacio(self, id_espacio: int, data: ActualizarEspacio) -> Espacio:
        espacio = self.obtener_espacio_id(id_espacio)
        return self.repo.actualizar_espacio(espacio, data)

    def eliminar_espacio(self, id_espacio: int) -> None:
        espacio = self.obtener_espacio_id(id_espacio)
        self.repo.eliminar_espacio(espacio)