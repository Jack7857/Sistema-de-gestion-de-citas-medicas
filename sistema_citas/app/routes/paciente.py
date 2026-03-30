from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Paciente
from app.schemas import PacienteCreate, PacienteUpdate, PacienteOut

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/", response_model=List[PacienteOut])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).all()


@router.get("/{cedula}", response_model=PacienteOut)
def obtener_paciente(cedula: str, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.cedula_paciente == cedula).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
    return paciente


@router.post("/", response_model=PacienteOut, status_code=status.HTTP_201_CREATED)
def crear_paciente(data: PacienteCreate, db: Session = Depends(get_db)):
    existente = db.query(Paciente).filter(Paciente.cedula_paciente == data.cedula_paciente).first()
    if existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un paciente con esa cédula")
    nuevo = Paciente(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{cedula}", response_model=PacienteOut)
def actualizar_paciente(cedula: str, data: PacienteUpdate, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.cedula_paciente == cedula).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(paciente, campo, valor)
    db.commit()
    db.refresh(paciente)
    return paciente


@router.delete("/{cedula}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_paciente(cedula: str, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.cedula_paciente == cedula).first()
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
    db.delete(paciente)
    db.commit()
