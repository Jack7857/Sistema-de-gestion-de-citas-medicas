from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Cita
from app.schemas import CitaCreate, CitaUpdate, CitaOut

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.get("/", response_model=List[CitaOut])
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()


@router.get("/{id_cita}", response_model=CitaOut)
def obtener_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    return cita


@router.post("/", response_model=CitaOut, status_code=status.HTTP_201_CREATED)
def crear_cita(data: CitaCreate, db: Session = Depends(get_db)):
    nueva = Cita(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put("/{id_cita}", response_model=CitaOut)
def actualizar_cita(id_cita: int, data: CitaUpdate, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cita, campo, valor)
    db.commit()
    db.refresh(cita)
    return cita


@router.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
