from fastapi import HTTPException, status

from app.models.espacios import Espacio
from app.repositories.espacio_rep import RepositorioEspacio
from app.schemas.espacio_schema import ActualizarEspacio, CrearEspacio

# Servicio para manejar la lógica de negocio relacionada con los espacios.

class EspacioService:
    def __init__(self, repo: RepositorioEspacio):
        self.repo = repo
    
    # Métodos del servicio para listar, obtener, crear, actualizar y eliminar espacios.
    def listar_espacios(
        self, pagina: int = 1, limite: int = 10, capacidad: int | None = None, disponibilidad: bool | None = None
    ) -> list[Espacio]:
        salto = (pagina - 1) * limite
        return self.repo.obtener_espacios(salto=salto, limite=limite, capacidad=capacidad, disponibilidad=disponibilidad)

    # Método para obtener un espacio por su ID, lanzando una excepción si no se encuentra.
    def obtener_espacio_id(self, id_espacio: int) -> Espacio:
        espacio = self.repo.obtener_espacio_id(id_espacio)
        if not espacio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="El espacio no existe"
            )
        return espacio

    # Metodos para crear espacios, con validaciones y manejo de excepciones.
    def crear_espacio(self, data: CrearEspacio) -> Espacio:
        # Se valida que la capacidad debe ser mayor a 0
        if data.capacidad <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La capacidad debe ser mayor a 0"
            )
        return self.repo.crear_espacio(data)

    # Método para actualizar un espacio.
    def actualizar_espacio(self, id_espacio: int, data: ActualizarEspacio) -> Espacio:
        espacio = self.obtener_espacio_id(id_espacio)
        return self.repo.actualizar_espacio(espacio, data)

    # Método para eliminar un espacio.
    def eliminar_espacio(self, id_espacio: int) -> None:
        espacio = self.obtener_espacio_id(id_espacio)
        self.repo.eliminar_espacio(espacio)