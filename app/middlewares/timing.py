import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Procesa la solicitud
        response = await call_next(request)
        
        # Calcula el tiempo transcurrido en segundos
        process_time = time.time() - start_time
        
        # Agrega la cabecera HTTP con el tiempo de respuesta en milisegundos
        response.headers["X-Process-Time"] = f"{process_time * 1000:.2f}ms"
        
        print(f"[LOG] {request.method} {request.url.path} completado en {process_time * 1000:.2f}ms con status {response.status_code}")
        
        return response
