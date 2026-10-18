from datetime import datetime, timedelta

from app.database import Base, SessionLocal, engine
from app.models.espacios import Espacio
from app.models.reservas import Reserva
from app.models.usuarios import Usuario


def poblar_base_de_datos():
    # Asegurar que las tablas existan
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("Iniciando la carga de datos iniciales")

        # Limpiar datos existentes para que sea reproducible
        db.query(Reserva).delete()
        db.query(Espacio).delete()
        db.query(Usuario).delete()
        db.commit()

        # Crear 5 Usuarios mínimos requeridos
        usuarios = [
            Usuario(nombre="Juan Perez", correo="juan.perez@ce.ucn.cl"),
            Usuario(nombre="Maria Gonzalez", correo="maria.gonzalez@alumnos.ucn.cl"),
            Usuario(nombre="Carlos Silva", correo="carlos.silva@ce.ucn.cl"),
            Usuario(nombre="Ana Morales", correo="ana.morales@alumnos.ucn.cl"),
            Usuario(nombre="Pedro Araya", correo="pedro.araya@ce.ucn.cl"),
        ]
        db.add_all(usuarios)
        db.commit()
        print(f"[OK] {len(usuarios)} Usuarios creados con exito.")

        # Crear 10 Espacios mínimos requeridos
        espacios = [
            Espacio(nombre="Auditorio Andres Sabella", ubicacion="Edificio F - Piso 1", capacidad=120, disponibilidad=True),
            Espacio(nombre="Sala de Estudio Grupal 1", ubicacion="Biblioteca Central - Piso 2", capacidad=8, disponibilidad=True),
            Espacio(nombre="Sala de Estudio Grupal 2", ubicacion="Biblioteca Central - Piso 2", capacidad=6, disponibilidad=True),
            Espacio(nombre="Laboratorio de Computacion 1", ubicacion="Pabellon K - Sala K-101", capacidad=35, disponibilidad=True),
            Espacio(nombre="Laboratorio de Computacion 2", ubicacion="Pabellon K - Sala K-102", capacidad=30, disponibilidad=True),
            Espacio(nombre="Sala de Conferencias DISIC", ubicacion="Edificio Sistemas - Piso 3", capacidad=40, disponibilidad=True),
            Espacio(nombre="Taller de Robotica", ubicacion="Pabellon I - Sala I-201", capacidad=15, disponibilidad=True),
            Espacio(nombre="Sala de Reuniones Decanato", ubicacion="Edificio Fundadores", capacidad=12, disponibilidad=True),
            Espacio(nombre="Coworking Estudiantes", ubicacion="Pabellon C - Piso 1", capacidad=25, disponibilidad=True),
            Espacio(nombre="Sala de Usos Multiples", ubicacion="Gimnasio Techado", capacidad=50, disponibilidad=False),
        ]
        db.add_all(espacios)
        db.commit()
        print(f"[OK] {len(espacios)} Espacios creados con exito.")

        db_usuarios = db.query(Usuario).all()
        db_espacios = db.query(Espacio).all()

        # Crear 15 Reservas mínimas requeridas (horarios sin solapamiento)
        hoy = datetime.now().date()
        reservas = []

        horarios = [
            (8, 10), (10, 12), (12, 14), (14, 16), (16, 18)
        ]

        res_count = 0
        for dia_offset in range(3): # Hoy, mañana y pasado mañana
            fecha_dia = datetime.combine(hoy + timedelta(days=dia_offset), datetime.min.time())
            for idx, (h_ini, h_fin) in enumerate(horarios):
                if res_count >= 15:
                    break
                
                usuario_asignado = db_usuarios[res_count % len(db_usuarios)]
                espacio_asignado = db_espacios[res_count % (len(db_espacios) - 1)] # Evitar el no disponible
                
                reserva = Reserva(
                    id_usuario=usuario_asignado.id,
                    id_espacio=espacio_asignado.id,
                    fecha=fecha_dia,
                    hora_inicio=fecha_dia.replace(hour=h_ini, minute=0),
                    hora_fin=fecha_dia.replace(hour=h_fin, minute=0),
                    estado="Confirmada" if res_count != 4 else "Cancelada"
                )
                reservas.append(reserva)
                res_count += 1

        db.add_all(reservas)
        db.commit()
        print(f"[OK] {len(reservas)} Reservas creadas con exito.")
        print("[EXITO] Base de datos poblada de forma reproducible exitosamente.")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error al poblar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    poblar_base_de_datos()
