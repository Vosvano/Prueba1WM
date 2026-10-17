from sqlalchemy.orm import Session

from app.models.usuarios import Usuario
from app.schemas.usuario_schema import ActualizarUsuario, CrearUsuario


class RepositorioUsuario:
    def __init__(self, db: Session):
        self.db = db

    def obtener_usuarios(self, salto: int = 0, limite: int = 10) -> list[Usuario]:
        return self.db.query(Usuario).offset(salto).limit(limite).all()
    
    def obtener_usuario_id(self, id_usuario: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == id_usuario).first()

    def obtener_usuario_correo(self, correo_usuario: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.correo == correo_usuario).first()

    def crear_usuario(self, datos_usuario: CrearUsuario) -> Usuario:
        nuevo_usuario = Usuario(**datos_usuario.model_dump())
        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario

    def actualizar_usuario(self, usuario: Usuario, usuario_data: ActualizarUsuario) -> Usuario:
        datos = usuario_data.model_dump(exclude_unset=True)
        for key, value in datos.items():
            setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
    
    def eliminar_usuario(self, usuario: Usuario) -> None:
        self.db.delete(usuario)
        self.db.commit()