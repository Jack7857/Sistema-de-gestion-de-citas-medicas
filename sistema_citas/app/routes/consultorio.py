from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Consultorio
from app.schemas import ConsultorioCreate, ConsultorioUpdate, ConsultorioOut

router = APIRouter(prefix="/consultorios", tags=["Consultorios"])


@router.get("/", response_model=List[ConsultorioOut])
def listar_consultorios(db: Session = Depends(get_db)):
    return db.query(Consultorio).all()


@router.get("/{id_consultorio}", response_model=ConsultorioOut)
def obtener_consultorio(id_consultorio: int, db: Session = Depends(get_db)):
    cons = db.query(Consultorio).filter(Consultorio.id_consultorio == id_consultorio).first()
    if not cons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consultorio no encontrado")
    return cons


@router.post("/", response_model=ConsultorioOut, status_code=status.HTTP_201_CREATED)
def crear_consultorio(data: ConsultorioCreate, db: Session = Depends(get_db)):
    nuevo = Consultorio(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id_consultorio}", response_model=ConsultorioOut)
def actualizar_consultorio(id_consultorio: int, data: ConsultorioUpdate, db: Session = Depends(get_db)):
    cons = db.query(Consultorio).filter(Consultorio.id_consultorio == id_consultorio).first()
    if not cons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consultorio no encontrado")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cons, campo, valor)
    db.commit()
    db.refresh(cons)
    return cons


@router.delete("/{id_consultorio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_consultorio(id_consultorio: int, db: Session = Depends(get_db)):
    cons = db.query(Consultorio).filter(Consultorio.id_consultorio == id_consultorio).first()
    if not cons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consultorio no encontrado")
    db.delete(cons)
    db.commit()
