from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.middlewares.timing import TimingMiddleware
from app.routers import espacios, reservas, usuarios

# Crear tablas en SQLite automáticamente al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Reservas de Espacios",
    description="Backend HTTP REST para sistema web y móvil - Cátedra I UCN",
    version="1.0.0"
)

# 1. Habilitar Middleware transversal (Tiempo de respuesta y logs) - 5 pts
app.add_middleware(TimingMiddleware)

# 2. Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# 3. Registrar los endpoints
app.include_router(espacios.router)
app.include_router(usuarios.router)
app.include_router(reservas.router)

@app.get("/")
def ruta_raiz():
    return {"mensaje": "Servidor HTTP en ejecución correctamente", "docs": "/docs"}