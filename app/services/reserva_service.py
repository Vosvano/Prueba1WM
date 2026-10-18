from datetime import date

from fastapi import HTTPException, status

from app.models.reservas import Reserva
from app.repositories.espacio_rep import RepositorioEspacio
from app.repositories.reserva_rep import RepositorioReserva
from app.repositories.usuario_rep import RepositorioUsuario
from app.schemas.reserva_schema import ActualizarReserva, CrearReserva

# Servicio para manejar la lógica de negocio relacionada con las reservas.

class ReservaService:
    def __init__(
        self,
        repo: RepositorioReserva,
        repo_usuario: RepositorioUsuario = None,
        repo_espacio: RepositorioEspacio = None
    ):
        self.repo = repo
        self.repo_usuario = repo_usuario
        self.repo_espacio = repo_espacio

    # Métodos del servicio para listar todas las reservas.
    def listar_reservas(
        self,
        pagina: int = 1,
        limite: int = 10,
        usuario_id: int | None = None,
        espacio_id: int | None = None,
        fecha: date | None = None,
        estado: str | None = None
    ) -> list[Reserva]:
        salto = (pagina - 1) * limite
        return self.repo.obtener_reservas(
            salto=salto,
            limite=limite,
            usuario_id=usuario_id,
            espacio_id=espacio_id,
            fecha=fecha,
            estado=estado
        )

    # Método para obtener una reserva por su ID, lanzando una excepción si no se encuentra.
    def obtener_reserva_id(self, id_reserva: int) -> Reserva:
        reserva = self.repo.obtener_reserva_id(id_reserva)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La reserva no existe"
            )
        return reserva

    # Método para crear una reserva, con validaciones de usuario, espacio y solapamiento de horarios.
    def crear_reserva(self, datos: CrearReserva) -> Reserva:

        # Validar que el usuario exista
        if self.repo_usuario:
            usuario = self.repo_usuario.obtener_usuario_id(datos.id_usuario)
            if not usuario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El usuario no existe"
                )

        # Validar que el espacio exista y esté disponible
        if self.repo_espacio:
            espacio = self.repo_espacio.obtener_espacio_id(datos.id_espacio)
            if not espacio:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El espacio no existe"
                )
            if not espacio.disponibilidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El espacio no se encuentra disponible actualmente"
                )

        # Validar horario lógico
        if datos.hora_inicio >= datos.hora_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora de inicio debe ser anterior a la hora de término"
            )

        # Impedir superposición de horarios
        fecha_reserva = datos.fecha.date()
        reservas_existentes = self.repo.obtener_reservas_activas_espacio(datos.id_espacio, fecha_reserva)

        for r in reservas_existentes:
            # Comprobación de solapamiento
            if datos.hora_inicio < r.hora_fin and datos.hora_fin > r.hora_inicio:
                inicio_str = r.hora_inicio.strftime("%H:%M")
                fin_str = r.hora_fin.strftime("%H:%M")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Horario no disponible: El espacio ya se encuentra reservado entre las {inicio_str} y {fin_str} hrs."
                )

        return self.repo.crear_reserva(datos)

    # Método para actualizar una reserva existente, con validaciones de solapamientos horarios.
    def actualizar_reserva(self, id_reserva: int, datos: ActualizarReserva) -> Reserva:
        reserva = self.obtener_reserva_id(id_reserva)
        nuevo_inicio = datos.hora_inicio or reserva.hora_inicio
        nuevo_fin = datos.hora_fin or reserva.hora_fin

        if nuevo_inicio >= nuevo_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora de inicio debe ser anterior a la hora de término"
            )

        fecha_reserva = (datos.fecha or reserva.fecha).date()
        reservas_existentes = self.repo.obtener_reservas_activas_espacio(reserva.id_espacio, fecha_reserva)

        for r in reservas_existentes:
            if r.id == reserva.id:
                continue 
            if nuevo_inicio < r.hora_fin and nuevo_fin > r.hora_inicio:
                inicio_str = r.hora_inicio.strftime("%H:%M")
                fin_str = r.hora_fin.strftime("%H:%M")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Conflicto de horario: El espacio ya tiene una reserva de {inicio_str} a {fin_str} hrs."
                )

        return self.repo.actualizar_reserva(reserva, datos)

    #Método para eliminar una reserva existente.
    def eliminar_reserva(self, id_reserva: int) -> None:
        reserva = self.obtener_reserva_id(id_reserva)
        self.repo.eliminar_reserva(reserva)
