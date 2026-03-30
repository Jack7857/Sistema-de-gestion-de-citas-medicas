from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routes import (
    especialidad_router,
    medico_router,
    paciente_router,
    consultorio_router,
    cita_router,
)

# Crea las tablas si no existen (útil en desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Citas",
    description="API REST para gestionar citas médicas",
    version="1.0.0",
)

# Registro de routers
app.include_router(especialidad_router)
app.include_router(medico_router)
app.include_router(paciente_router)
app.include_router(consultorio_router)
app.include_router(cita_router)


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "Bienvenido al Sistema de Gestión de Citas 🏥"}
