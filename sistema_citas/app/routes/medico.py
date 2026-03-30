from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Medico
from app.schemas import MedicoCreate, MedicoUpdate, MedicoOut

router = APIRouter(prefix="/medicos", tags=["Médicos"])


@router.get("/", response_model=List[MedicoOut])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(Medico).all()


@router.get("/{id_medico}", response_model=MedicoOut)
def obtener_medico(id_medico: int, db: Session = Depends(get_db)):
    medico = db.query(Medico).filter(Medico.id_medico == id_medico).first()
    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado")
    return medico


@router.post("/", response_model=MedicoOut, status_code=status.HTTP_201_CREATED)
def crear_medico(data: MedicoCreate, db: Session = Depends(get_db)):
    nuevo = Medico(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id_medico}", response_model=MedicoOut)
def actualizar_medico(id_medico: int, data: MedicoUpdate, db: Session = Depends(get_db)):
    medico = db.query(Medico).filter(Medico.id_medico == id_medico).first()
    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(medico, campo, valor)
    db.commit()
    db.refresh(medico)
    return medico


@router.delete("/{id_medico}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_medico(id_medico: int, db: Session = Depends(get_db)):
    medico = db.query(Medico).filter(Medico.id_medico == id_medico).first()
    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado")
    db.delete(medico)
    db.commit()
