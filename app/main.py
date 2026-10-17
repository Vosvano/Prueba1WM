from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import spaces

# Crear tablas en SQLite automáticamente al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Reservas y Consultas",
    description="Backend HTTP REST para sistema web/móvil",
    version="1.0.0"
)

# Habilitar CORS (Crucial para Web y Móvil)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Registrar los endpoints
app.include_router(spaces.router)

@app.get("/")
def ruta_raiz():
    return {"mensaje": "Servidor HTTP en ejecución correctamente"}